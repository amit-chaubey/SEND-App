from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from functools import wraps
import time

word_blueprint = Blueprint('word', __name__)

# Pre-categorize words by length
def categorize_words(words):
    return {
        'Easy': [w for w in words if len(w) <= 5],
        'Medium': [w for w in words if 5 < len(w) <= 7],
        'Hard': [w for w in words if len(w) > 7]
    }

# Define FALLBACK_WORDS first
FALLBACK_WORDS = {
    'th': ['think', 'three', 'thumb', 'thrill', 'thunder', 'thank', 'thick', 'thin', 'throw', 'theme',
           'third', 'throne', 'thought', 'threat', 'thirst', 'thread', 'thief', 'thing', 'theater'],
    'sh': ['ship', 'wish', 'shop', 'shine', 'shower', 'shell', 'share', 'shoe', 'show', 'shut',
           'shade', 'shape', 'sharp', 'sheep', 'sheet', 'shelf', 'shoot', 'shore', 'short'],
    'wh': ['what', 'when', 'where', 'which', 'whale', 'wheel', 'white', 'while', 'whip', 'why',
           'whisper', 'whistle', 'whole', 'whose', 'wharf', 'wheat', 'whirl'],
    'ng': ['sing', 'ring', 'king', 'strong', 'wrong', 'long', 'young', 'bring', 'wing', 'song',
           'spring', 'string', 'singing', 'running', 'ringing', 'falling', 'evening']
}

# Then define CATEGORIZED_WORDS
CATEGORIZED_WORDS = {
    'ch': categorize_words([
        # Easy words (≤5 letters)
        'chair', 'chest', 'chin', 'chip', 'chat',
        # Medium words (6-7 letters)
        'church', 'cheese', 'chicken', 'change', 'charter',
        # Hard words (>7 letters)
        'champion', 'chocolate', 'chairman', 'cheerful', 'checking'
    ]),
    'ph': categorize_words([
        # Easy words (≤5 letters)
        'phone', 'photo', 'graph', 'phase', 'phil',
        # Medium words (6-7 letters)
        'physics', 'phantom', 'pharaoh', 'phonics',
        # Hard words (>7 letters)
        'phonetic', 'pharmacy', 'phosphate', 'physical', 'phonecard'
    ]),
    'th': categorize_words(FALLBACK_WORDS['th']),
    'sh': categorize_words(FALLBACK_WORDS['sh']),
    'wh': categorize_words(FALLBACK_WORDS['wh']),
    'ng': categorize_words(FALLBACK_WORDS['ng'])
}

# Simple rate limiting with per-sound tracking
RATE_LIMIT = {}
RATE_LIMIT_PERIOD = 0.5

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        sound = request.args.get('sound', '')
        key = f"{ip}:{sound}"
        current_time = time.time()
        
        if key in RATE_LIMIT:
            last_request_time = RATE_LIMIT[key]
            if current_time - last_request_time < RATE_LIMIT_PERIOD:
                time.sleep(RATE_LIMIT_PERIOD - (current_time - last_request_time))
        
        RATE_LIMIT[key] = current_time
        return f(*args, **kwargs)
    return decorated_function

@word_blueprint.route('/words-by-sound', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_words_by_sound():
    """Get words for a specific sound pattern."""
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        sound = request.args.get('sound', '').lower()
        if not sound:
            return jsonify({'error': 'Sound parameter is required'}), 400
        
        if sound in CATEGORIZED_WORDS:
            return jsonify({'words': CATEGORIZED_WORDS[sound]})
        
        return jsonify({'error': f'No words found for sound "{sound}"'}), 404
    except Exception as e:
        print(f"Error in get_words_by_sound: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@word_blueprint.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@word_blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200