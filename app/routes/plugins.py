from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Plugin
from app.plugin_loader import load_plugins

plugins_bp = Blueprint('plugins', __name__)
plugins = load_plugins()

@plugins_bp.route('/plugins', methods=['GET'])
def get_plugins():
    plugins = Plugin.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in plugins]), 200

@plugins_bp.route('/plugins/load', methods=['POST'])
@jwt_required()
def load_plugin():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'msg': 'Missing name'}), 400
    plugin = Plugin(name=data['name'], description=data.get('description', ''))
    db.session.add(plugin)
    db.session.commit()
    return jsonify({'id': plugin.id}), 200

@plugins_bp.route('/plugins/unload', methods=['POST'])
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

@plugins_bp.route('/plugins/<plugin_name>/run', methods=['POST'])
def run_plugin(plugin_name):
    plugin = plugins.get(plugin_name)
    if not plugin:
        return jsonify({'error': 'Plugin not found'}), 404
    data = request.get_json() or {}
    result = plugin.run(data)
    return jsonify(result), 200
