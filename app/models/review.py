from datetime import datetime, timezone
from app import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    reading_format = db.Column(db.String(20), nullable=False)  # paperback, audiobook, ebook
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'review_text': self.review_text,
            'reading_format': self.reading_format,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
