from datetime import datetime, timezone
from app import db

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    publication_date = db.Column(db.DateTime)
    page_count = db.Column(db.Integer)
    language = db.Column(db.String(10), default='en')
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    author = db.relationship("Author", back_populates="books")
    comments = db.relationship("Comment", back_populates="book", lazy=True)
    ratings = db.relationship("Rating", back_populates="book", lazy=True)
    tags = db.relationship("Tag", secondary="book_tags", back_populates="books")
