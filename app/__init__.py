from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

def create_app():
    # Use absolute path for Render deployment
    static_folder = '/opt/render/project/src/frontend/build'
    if not os.path.exists(static_folder):
        # Fallback to local development path
        static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
    
    app.logger.info(f"Using static folder: {static_folder}")
    
    app = Flask(__name__, 
                static_folder=static_folder,
                static_url_path='')
    CORS(app)

    # Import and register blueprints
    from app.routes.word_routes import word_blueprint
    app.register_blueprint(word_blueprint, url_prefix='/api')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        try:
            app.logger.info(f"Serving path: {path}")
            app.logger.info(f"Static folder exists: {os.path.exists(app.static_folder)}")
            
            if path.startswith('api/'):
                return {"error": "Not found"}, 404
            
            # List directory contents for debugging
            app.logger.info(f"Directory contents: {os.listdir(app.static_folder)}")
            
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            
            index_path = os.path.join(app.static_folder, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(app.static_folder, 'index.html')
            else:
                app.logger.error(f"index.html not found in {app.static_folder}")
                return {"error": "Application not properly built"}, 500

        except Exception as e:
            app.logger.error(f"Error serving static files: {str(e)}")
            return {"error": str(e)}, 500

    @app.errorhandler(404)
    def not_found_error(error):
        return send_from_directory(app.static_folder, 'index.html')

    return app