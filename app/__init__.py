from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

def create_app():
    # Get absolute path to the build directory
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
    
    # Verify if the build directory exists
    if not os.path.exists(static_folder):
        os.makedirs(static_folder, exist_ok=True)
        print(f"Created static folder at: {static_folder}")
    
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
            # Debug logging
            app.logger.info(f"Serving path: {path}")
            app.logger.info(f"Static folder: {app.static_folder}")
            
            # Handle API routes
            if path.startswith('api/'):
                return {"error": "Not found"}, 404

            # Try to serve the specific file
            if path:
                file_path = os.path.join(app.static_folder, path)
                if os.path.exists(file_path):
                    app.logger.info(f"Serving file: {file_path}")
                    return send_from_directory(app.static_folder, path)

            # Serve index.html
            index_path = os.path.join(app.static_folder, 'index.html')
            if os.path.exists(index_path):
                app.logger.info(f"Serving index.html from: {index_path}")
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