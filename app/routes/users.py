from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/register', methods=['POST'])
def register():
    """User registration
    ---
    tags:
        - Users
    """
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'msg': 'Missing fields'}), 400
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'User exists'}), 409
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered'}), 201

@users_bp.route('/users/login', methods=['POST'])
def login():
    """User login
    ---
    tags:
        - Users
    """
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users
    ---
    tags:
        - Users
    """
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in users
    ]), 200

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a user by ID
    ---
    tags:
        - Users
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user by ID
    ---
    tags:
        - Users
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'User deleted'}), 200
