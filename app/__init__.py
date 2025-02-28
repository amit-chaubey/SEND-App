from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables at startup
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
    app.debug = True
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register blueprint
    from app.routes.word_routes import word_blueprint
    app.register_blueprint(word_blueprint, url_prefix='/api')

    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path.startswith('api'):
            return {"error": "Not Found"}, 404
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app 