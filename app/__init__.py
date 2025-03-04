from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/build',
                static_url_path='')
    CORS(app)

    # Import and register blueprints
    from app.routes.word_routes import word_blueprint
    app.register_blueprint(word_blueprint, url_prefix='/api')

    # Serve React App - handle all routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        try:
            if path.startswith('api/'):
                return {"error": "Not found"}, 404
                
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
                
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error serving static files: {str(e)}")
            return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')

    return app