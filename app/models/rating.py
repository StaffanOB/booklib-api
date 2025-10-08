from datetime import datetime, timezone
from app import db

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="ratings")
    book = db.relationship("Book", back_populates="ratings")
    
    __table_args__ = (
        db.UniqueConstraint("book_id", "user_id", name="unique_book_user_rating"),
    )
