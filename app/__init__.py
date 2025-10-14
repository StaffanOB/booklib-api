from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)
    jwt.init_app(app)
    
    @app.route("/health")
    def health_check():
        from app.db_utils import get_health_status
        return get_health_status()
    
    from app.routes import users_bp, books_bp, tags_bp, comments_bp, ratings_bp, plugins_bp, protected_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp) 
    app.register_blueprint(tags_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(plugins_bp)
    app.register_blueprint(protected_bp)
    from app.swagger import swaggerui_blueprint, docs
    app.register_blueprint(swaggerui_blueprint, url_prefix="/docs")
    app.register_blueprint(docs)
    return app
