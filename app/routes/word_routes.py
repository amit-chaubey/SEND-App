from flask import Blueprint, request, jsonify
from app.models import Word
from app import db
from app.services.gpt_service import fetch_word_from_gpt

word_blueprint = Blueprint('word', __name__)

# In word route (Flask)
import re

@word_blueprint.route('/', methods=['POST'])
def get_word():
    data = request.json
    focus_sound = data.get('focus_sound')
    difficulty_level = data.get('difficulty_level', 1)

    print(f"Fetching word with focus_sound: {focus_sound}, difficulty_level: {difficulty_level}")
    
    try:
        gpt_response = fetch_word_from_gpt(focus_sound, difficulty_level)
        print(f"GPT Response: {gpt_response}")

        # Sanitize the response to extract the word
        word_match = re.search(r'"(.*?)"', gpt_response)  # Extract word inside double quotes
        if word_match:
            word = word_match.group(1).strip().lower()
        else:
            word = gpt_response.strip().lower()  # Fallback in case no quotes are found

        if word:
            return jsonify({"word": word}), 200
        else:
            return jsonify({"error": "Failed to extract word from GPT response"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500



def sanitize_openai_response(response):
    """
    Extract the core word from the OpenAI response.
    Example: 'The word "fish" contains...' -> 'fish'
    """
    import re
    match = re.search(r'"\b(\w+)\b"', response)  # Look for word inside quotes
    if match:
        return match.group(1).lower()  # Return the word in lowercase
    return response.strip().lower()
