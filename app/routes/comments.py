from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Comment

comments_bp = Blueprint('comments', __name__)

# Get comments for a book endpoint
@comments_bp.route('/books/<int:id>/comments', methods=['GET'])
def get_comments(id):
    """Get comments for a book
    ---
    tags:
        - Comments
    """
    comments = Comment.query.filter_by(book_id=id).all()
    return jsonify([{'id': c.id, 'content': c.content, 'user_id': c.user_id} for c in comments]), 200

# Add comment for a book endpoint
@comments_bp.route('/books/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_comment(id):
    """Add a comment for a book
    ---
    tags:
        - Comments
    """
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'msg': 'Missing content'}), 400
    user_id = get_jwt_identity()
    comment = Comment(book_id=id, user_id=user_id, content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'id': comment.id}), 201

# Update comment endpoint
@comments_bp.route('/books/<int:id>/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(id, comment_id): 
    """Update a comment for a book
    ---
    tags:
        - Comments
    """
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'msg': 'Missing content'}), 400
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, book_id=id, user_id=user_id).first()
    if not comment:
        return jsonify({'msg': 'Comment not found'}), 404
    comment.content = data['content']
    db.session.commit()
    return jsonify({'id': comment.id, 'content': comment.content}), 200

# Delete comment endpoint
@comments_bp.route('/books/<int:id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id, comment_id):
    """Delete a comment for a book
    ---
    tags:
        - Comments
    """
    user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, book_id=id, user_id=user_id).first()
    if not comment:
        return jsonify({'msg': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'msg': 'Comment deleted'}), 200
