from flask import Flask, send_from_directory
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
            # First, try to find the file in static folder
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            # For API routes, let them be handled by blueprint
            if path.startswith('api/'):
                return app.send_static_file('index.html')
            # For all other routes, serve the React app
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error serving static files: {str(e)}")
            return app.send_static_file('index.html')

    return app