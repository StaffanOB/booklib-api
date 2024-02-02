import os
import tempfile
import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db
from models import UserModel

from models import UserModel

@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_app_creation(client):
    response = client.get('/')
    assert response.status_code == 404  # The root URL should return a 404



