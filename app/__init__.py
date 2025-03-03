from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    # Initialize Flask app with static files configuration
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    CORS(app)
    load_dotenv()

    # Import and register blueprints
    from app.routes.word_routes import word_blueprint
    app.register_blueprint(word_blueprint, url_prefix='/api')

    # Serve React App - catch all routes and redirect to index.html
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app 