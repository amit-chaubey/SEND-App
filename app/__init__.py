from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///spelling_app.db")  # Use .env variable or default
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Static files and templates configuration
    app.static_folder = "static"
    app.template_folder = "templates"

    # Register blueprints
    from app.routes.main_routes import main_blueprint
    from app.routes.word_routes import word_blueprint
    from app.routes.user_routes import user_blueprint
    from app.routes.score_routes import score_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')  # Root route
    app.register_blueprint(word_blueprint, url_prefix='/word')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(score_blueprint, url_prefix='/score')

    return app
