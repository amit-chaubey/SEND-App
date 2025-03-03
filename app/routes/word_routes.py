from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from functools import wraps
import time

word_blueprint = Blueprint('word', __name__)

# Fallback words dictionary - comprehensive list for each sound
FALLBACK_WORDS = {
    'th': ['think', 'three', 'thumb', 'thrill', 'thunder', 'thank', 'thick', 'thin', 'throw', 'theme'],
    'sh': ['ship', 'wish', 'shop', 'shine', 'shower', 'shell', 'share', 'shoe', 'show', 'shut'],
    'ch': ['chair', 'watch', 'church', 'cheese', 'chicken', 'child', 'chest', 'beach', 'teach', 'lunch'],
    'ph': ['phone', 'graph', 'photo', 'phrase', 'dolphin', 'elephant', 'nephew', 'physics', 'alphabet', 'pharmacy'],
    'wh': ['what', 'when', 'where', 'which', 'whale', 'wheel', 'white', 'while', 'whip', 'why'],
    'ng': ['sing', 'ring', 'king', 'strong', 'wrong', 'long', 'young', 'bring', 'wing', 'song']
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
@rate_limit
def get_words_by_sound():
    if request.method == 'OPTIONS':
        return '', 200
        
    sound = request.args.get('sound', '').lower()
    if not sound:
        return jsonify({'error': 'Sound parameter is required'}), 400
    
    count = int(request.args.get('count', default=50))
    
    # Always use fallback words
    if sound in FALLBACK_WORDS:
        words = FALLBACK_WORDS[sound]
        return jsonify({'words': words[:count]})
    
    return jsonify({'error': f'No words found for sound "{sound}"'}), 404

@word_blueprint.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200

@word_blueprint.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200