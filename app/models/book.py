from datetime import datetime, timezone
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(32), unique=True)  # Added
    description = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    series = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    comments = db.relationship("Comment", backref="book", lazy=True)
    ratings = db.relationship("Rating", backref="book", lazy=True)
    tags = db.relationship("Tag", secondary="book_tags", back_populates="books")
    authors = db.relationship('Author', secondary='book_author', backref='books')

    cover_url = db.Column(db.String(512))  # URL for book cover image
