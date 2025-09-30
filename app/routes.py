from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import db
from app.models import User, Book, Tag, Comment, Rating, Plugin
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# User registration
@api.route('/users/register', methods=['POST'])
def register():


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

# User login
@api.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

# Protected example endpoint
@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({'msg': f'Hello user {user_id}'}), 200

# Books endpoints
@api.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'description': b.description,
            'publish_year': b.publish_year,
            'series': b.series
        } for b in books
    ]), 200

@api.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author')):
        return jsonify({'msg': 'Missing fields'}), 400
    if not data['title'].strip() or not data['author'].strip():
        return jsonify({'msg': 'Title and author cannot be empty'}), 400
    book = Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description', ''),
        publish_year=data.get('publish_year'),
        series=data.get('series')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id}), 201

# Tags endpoints
@api.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tags]), 200

@api.route('/tags', methods=['POST'])
@jwt_required()
def add_tag():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify({'id': tag.id}), 201

# Comments endpoints
@api.route('/books/<int:id>/comments', methods=['GET'])
def get_comments(id):
    comments = Comment.query.filter_by(book_id=id).all()
    return jsonify([{'id': c.id, 'text': c.text, 'user_id': c.user_id} for c in comments]), 200

@api.route('/books/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_comment(id):
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'msg': 'Missing text'}), 400
    user_id = get_jwt_identity()
    comment = Comment(book_id=id, user_id=user_id, text=data['text'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'id': comment.id}), 201

# Ratings endpoints
@api.route('/books/<int:id>/ratings', methods=['GET'])
def get_ratings(id):
    ratings = Rating.query.filter_by(book_id=id).all()
    if not ratings:
        return jsonify({'average': None}), 200
    avg = sum(r.value for r in ratings) / len(ratings)
    return jsonify({'average': avg}), 200

@api.route('/books/<int:id>/ratings', methods=['POST'])
@jwt_required()
def add_rating(id):
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'msg': 'Missing value'}), 400
    user_id = get_jwt_identity()
    rating = Rating(book_id=id, user_id=user_id, value=data['value'])
    db.session.add(rating)
    db.session.commit()
    return jsonify({'id': rating.id}), 201

# Plugins endpoints
@api.route('/plugins', methods=['GET'])
def get_plugins():
    plugins = Plugin.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in plugins]), 200

@api.route('/plugins/load', methods=['POST'])
@jwt_required()
def load_plugin():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    # Plugin loading logic placeholder
    plugin = Plugin(name=data['name'], description=data.get('description', ''))
    db.session.add(plugin)
    db.session.commit()
    return jsonify({'id': plugin.id}), 200

@api.route('/plugins/unload', methods=['POST'])
@jwt_required()
def unload_plugin():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    plugin = Plugin.query.filter_by(name=data['name']).first()
    if not plugin:
        return jsonify({'msg': 'Plugin not found'}), 404
    db.session.delete(plugin)
    db.session.commit()
    return jsonify({'msg': 'Plugin unloaded'}), 200

# User deletion
@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'User deleted'}), 200

@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in users
    ]), 200

@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
