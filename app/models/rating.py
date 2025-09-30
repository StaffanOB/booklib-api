from datetime import datetime, timezone
from app import db

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    __table_args__ = (
        db.UniqueConstraint("book_id", "user_id", name="unique_book_user_rating"),
    )
