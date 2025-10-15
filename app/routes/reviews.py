from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Review, Book, User
from app.db_utils import handle_db_errors

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('', methods=['GET'])
@handle_db_errors
def get_all_reviews():
    """Get all reviews"""
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/<int:review_id>', methods=['GET'])
@handle_db_errors
def get_review(review_id):
    """Get a specific review by ID"""
    review = Review.query.get_or_404(review_id)
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/book/<int:book_id>', methods=['GET'])
@handle_db_errors
def get_book_reviews(book_id):
    """Get all reviews for a specific book"""
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/user/<int:user_id>', methods=['GET'])
@handle_db_errors
def get_user_reviews(user_id):
    """Get all reviews by a specific user"""
    user = User.query.get_or_404(user_id)
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('', methods=['POST'])
@jwt_required()
@handle_db_errors
def create_review():
    """Create a new review (requires authentication)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not data or 'book_id' not in data or 'review_text' not in data or 'reading_format' not in data:
        return jsonify({'error': 'Missing required fields: book_id, review_text, reading_format'}), 400
    
    # Validate reading format
    valid_formats = ['paperback', 'audiobook', 'ebook']
    if data['reading_format'] not in valid_formats:
        return jsonify({'error': f'Invalid reading_format. Must be one of: {", ".join(valid_formats)}'}), 400
    
    # Check if book exists
    book = Book.query.get_or_404(data['book_id'])
    
    # Check if user already reviewed this book
    existing_review = Review.query.filter_by(
        book_id=data['book_id'],
        user_id=current_user_id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this book. Use PUT to update your review.'}), 400
    
    # Create new review
    review = Review(
        book_id=data['book_id'],
        user_id=current_user_id,
        review_text=data['review_text'],
        reading_format=data['reading_format']
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify(review.to_dict()), 201

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
@handle_db_errors
def update_review(review_id):
    """Update an existing review (only by the review owner)"""
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    
    # Check if current user owns this review
    if review.user_id != current_user_id:
        return jsonify({'error': 'You can only update your own reviews'}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if 'review_text' in data:
        review.review_text = data['review_text']
    
    if 'reading_format' in data:
        valid_formats = ['paperback', 'audiobook', 'ebook']
        if data['reading_format'] not in valid_formats:
            return jsonify({'error': f'Invalid reading_format. Must be one of: {", ".join(valid_formats)}'}), 400
        review.reading_format = data['reading_format']
    
    db.session.commit()
    
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
@handle_db_errors
def delete_review(review_id):
    """Delete a review (only by the review owner)"""
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    
    # Check if current user owns this review
    if review.user_id != current_user_id:
        return jsonify({'error': 'You can only delete your own reviews'}), 403
    
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted successfully'}), 200
