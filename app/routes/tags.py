from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Tag

import json
import os

def ensure_default_tags():
    resource_path = os.path.join(os.path.dirname(__file__), '../resources/tags.json')
    with open(resource_path, 'r') as f:
        required_tags = json.load(f)
    for tag_name in required_tags:
        if not Tag.query.filter_by(name=tag_name).first():
            db.session.add(Tag(name=tag_name))
    db.session.commit()

tags_bp = Blueprint('tags', __name__)


# Get all tags endpoint
@tags_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags
    ---
    tags:
        - Tags
    """
    tags = Tag.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tags]), 200

# Add new tag endpoint
@tags_bp.route('/tags', methods=['POST'])
@jwt_required()
def add_tag():
    """Add a new tag
    ---
    tags:
        - Tags
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify({'id': tag.id, 'name': tag.name}), 201

# Update tag endpoint
@tags_bp.route('/tags/<int:id>', methods=['PUT'])
@jwt_required()
def update_tag(id):
    """Update a tag
    ---
    tags:
        - Tags
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({'msg': 'Tag not found'}), 404
    tag.name = data['name']
    db.session.commit()
    return jsonify({'id': tag.id, 'name': tag.name}), 200

# Delete tag endpoint
@tags_bp.route('/tags/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tag(id):
    """Delete a tag
    ---
    tags:
        - Tags
    """
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({'msg': 'Tag not found'}), 404
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'msg': 'Tag deleted'}), 200