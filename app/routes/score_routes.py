from flask import Blueprint, request, jsonify
from app.models import User, Attempt, Word, Score  # Assuming these models are correctly defined
from app import db

score_blueprint = Blueprint("score", __name__)

@score_blueprint.route("/submit", methods=["POST"])
def submit_score():
    try:
        data = request.json
        user_id = data.get("user_id")
        word_id = data.get("word_id")
        score = data.get("score")

        if not (user_id and word_id and score is not None):
            return jsonify({"error": "Invalid data."}), 400

        # Create and save the attempt
        attempt = Attempt(user_id=user_id, word_id=word_id, score=score)
        db.session.add(attempt)

        # Update user total score
        user = User.query.get(user_id)
        if user:
            user.total_score += score
            user.difficulty_level = (
                user.difficulty_level + 1 if score >= 70 else max(1, user.difficulty_level - 1)
            )
            db.session.commit()
            return jsonify({"message": "Score submitted successfully."}), 200
        else:
            return jsonify({"error": "User not found."}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Error in /submit: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@score_blueprint.route("/calculate", methods=["POST"])
def calculate_score():
    try:
        data = request.json
        user_word = data.get("user_word", "").strip().lower()
        correct_word = data.get("correct_word", "").strip().lower()

        if not user_word or not correct_word:
            return jsonify({"error": "Both user_word and correct_word are required."}), 400

        score = len(set(user_word).intersection(correct_word)) / max(len(correct_word), len(user_word)) * 100

        return jsonify({"score": round(score, 2)}), 200
    except Exception as e:
        print(f"Error in /calculate: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@score_blueprint.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        # Fetch top scores ordered by total_score descending
        scores = Score.query.order_by(Score.total_score.desc()).limit(10).all()  # Adjust limit as needed
        leaderboard = [
            {"username": score.username, "total_score": score.total_score}
            for score in scores
        ]
        return jsonify({"leaderboard": leaderboard}), 200
    except Exception as e:
        print(f"Error in /leaderboard: {e}")
        return jsonify({"error": "Failed to fetch leaderboard data."}), 500


@score_blueprint.route("/", methods=["POST"])
def update_score():
    try:
        data = request.json
        is_correct = data.get("correct")
        username = data.get("username", "Guest")  # Default to "Guest" if no username provided

        if is_correct is None:
            return jsonify({"error": "Missing 'correct' field in request"}), 400

        # Find or create the user's score entry
        score = Score.query.filter_by(username=username).first()
        if not score:
            score = Score(username=username, total_score=0)
            db.session.add(score)

        # Update score if correct
        if is_correct:
            score.total_score += 10  # Add points for a correct answer

        db.session.commit()

        return jsonify({"message": "Score updated successfully", "score": score.total_score}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in /update_score: {e}")
        return jsonify({"error": "Failed to update score"}), 500
