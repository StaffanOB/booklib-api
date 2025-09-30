from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Rating

ratings_bp = Blueprint('ratings', __name__)

# Get ratings for a book endpoint
@ratings_bp.route('/books/<int:id>/ratings', methods=['GET'])
def get_ratings(id):
    """Get average rating for a book
    ---
    tags:
        - Ratings
    """
    ratings = Rating.query.filter_by(book_id=id).all()
    if not ratings:
        return jsonify({'average': None}), 200
    avg = sum(r.rating for r in ratings) / len(ratings)
    return jsonify({'id': id, 'average': avg}), 200

# Add rating for a book endpoint
@ratings_bp.route('/books/<int:id>/ratings', methods=['POST'])
@jwt_required()
def add_rating(id):
    """Add a rating for a book
    ---
    tags:
        - Ratings
    """
    data = request.get_json()
    if not data or 'rating' not in data:
        return jsonify({'msg': 'Missing rating'}), 400
    user_id = get_jwt_identity()
    existing = Rating.query.filter_by(book_id=id, user_id=user_id).first()
    if existing:
        return jsonify({'msg': 'User has already rated this book'}), 409
    rating = Rating(book_id=id, user_id=user_id, rating=data['rating'])
    db.session.add(rating)
    db.session.commit()
    return jsonify({'id': rating.id}), 201

# Update rating for a book endpoint
@ratings_bp.route('/books/<int:id>/ratings/<int:rating_id>', methods=['PUT'])
@jwt_required()
def update_rating(id, rating_id):
    """Update a rating for a book
    ---
    tags:
        - Ratings
    """
    data = request.get_json()
    if not data or 'rating' not in data:
        return jsonify({'msg': 'Missing rating'}), 400
    user_id = get_jwt_identity()
    rating = Rating.query.filter_by(id=rating_id, book_id=id, user_id=user_id).first()
    if not rating:
        return jsonify({'msg': 'Rating not found'}), 404
    rating.rating = data['rating']
    db.session.commit()
    return jsonify({'msg': 'Rating updated'}), 200

# Delete rating for a book endpoint
@ratings_bp.route('/books/<int:id>/ratings/<int:rating_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(id, rating_id):
    """Delete a rating for a book
    ---
    tags:
        - Ratings
    """
    user_id = get_jwt_identity()
    rating = Rating.query.filter_by(id=rating_id, book_id=id, user_id=user_id).first()
    if not rating:
        return jsonify({'msg': 'Rating not found'}), 404
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'msg': 'Rating deleted'}), 200