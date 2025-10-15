from datetime import datetime, timezone
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships with explicit foreign keys
    comments = db.relationship("Comment", back_populates="user", lazy=True)
    ratings = db.relationship("Rating", back_populates="user", lazy=True)
    reviews = db.relationship("Review", back_populates="user", lazy=True)
