from flask import Blueprint, request, jsonify, Flask
from app.models import User, Attempt, Word
from app import db

# Define Blueprint
user_blueprint = Blueprint('user', __name__)

# Route: Register a new user
@user_blueprint.route('/', methods=['POST'])
def register_user():
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({"error": "Username is required."}), 400

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists."}), 409  # Conflict status code

        # Create a new user
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully.", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": "An error occurred during registration.", "details": str(e)}), 500

# Route: Fetch user history
@user_blueprint.route('/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    try:
        # Retrieve the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Retrieve the user's attempts
        attempts = Attempt.query.filter_by(user_id=user_id).all()
        history = [
            {
                "word": Word.query.get(attempt.word_id).word if Word.query.get(attempt.word_id) else None,
                "score": attempt.score,
                "timestamp": attempt.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
            }
            for attempt in attempts
        ]

        return jsonify({"username": user.username, "history": history}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching history.", "details": str(e)}), 500


from flask import Blueprint

# Define a Blueprint for the root route
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the Spelling App API!"}, 200
