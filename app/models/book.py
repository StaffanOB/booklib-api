from datetime import datetime, timezone
from app import db

# Association table for many-to-many relationship between books and authors
book_authors = db.Table('book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    publication_date = db.Column(db.DateTime)
    publish_year = db.Column(db.Integer)
    series = db.Column(db.String(255))
    cover_url = db.Column(db.String(512))
    page_count = db.Column(db.Integer)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    authors = db.relationship("Author", secondary="book_authors", back_populates="books")
    comments = db.relationship("Comment", back_populates="book", lazy=True)
    ratings = db.relationship("Rating", back_populates="book", lazy=True)
    reviews = db.relationship("Review", back_populates="book", lazy=True)
    tags = db.relationship("Tag", secondary="book_tags", back_populates="books")
