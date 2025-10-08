from datetime import datetime, timezone
from app import db

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.Text)
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    books = db.relationship("Book", back_populates="author")
