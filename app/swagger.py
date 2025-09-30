from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "BookLib API"
    }
)

docs = Blueprint('docs', __name__)

@docs.route('/static/swagger.json')
def swagger_json():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'swagger.json')
