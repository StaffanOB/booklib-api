import pytest
from app import create_app, db
from app.models import User, Book

@pytest.fixture
def app():
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
    return app.test_client()

def test_user_can_add_and_get_book(client):
    # Register a user
    response = client.post('/users/register', json={
        'username': 'integrationuser',
        'email': 'integrationuser@example.com',
        'password': 'integrationpass'
    })
    assert response.status_code == 201

    # Login to get JWT
    response = client.post('/users/login', json={
        'username': 'integrationuser',
        'password': 'integrationpass'
    })
    assert response.status_code == 200
    token = response.get_json()['access_token']

    # Add a book
    response = client.post('/books', json={
        'title': 'Integration Book',
        'authors': ['Integration Author'],
        'description': 'Integration test book.',
        'cover_url': 'http://example.com/cover.jpg'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    book_id = response.get_json()['id']

    # Get the book
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Integration Book'
    assert 'Integration Author' in data['author'] or 'Integration Author' in data.get('authors', [])
    assert data.get('cover_url') == 'http://example.com/cover.jpg'
