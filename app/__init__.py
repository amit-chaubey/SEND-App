from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

def create_app():
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
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
            # For API routes, let the blueprint handle it
            if path.startswith('api/'):
                return app.send_static_file('index.html')
            
            # Try to serve the specific file
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            
            # Default to index.html
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
    def not_found(e):
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error in 404 handler: {str(e)}")
            return {"error": "Page not found"}, 404

    return app