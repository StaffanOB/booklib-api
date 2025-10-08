import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

def test_get_books_returns_200(client):
    """Test that GET /books returns 200 status code."""
    response = client.get('/books')
    assert response.status_code == 200