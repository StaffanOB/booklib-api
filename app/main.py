"""
BookLib API main entry point.

This application is a RESTful API for managing books, users, tags, comments, ratings, and plugins.
It uses Flask, SQLAlchemy, and JWT authentication. Run this file to start the development server.
"""
from flask_migrate import Migrate
from app import create_app, db
from app.routes import (
    users_bp, books_bp, tags_bp, comments_bp, ratings_bp, plugins_bp, protected_bp
)

app = create_app()
migrate = Migrate(app, db)


if __name__ == '__main__':
    with app.app_context():
        # Ensure all models are imported before creating tables
        from app.models import User, Book, Tag, BookTag, Comment, Rating, Plugin
        db.create_all()
        from app.routes.tags import ensure_default_tags
        ensure_default_tags()
    app.run(debug=True)
