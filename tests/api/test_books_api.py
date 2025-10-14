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

def test_get_book_by_id(client):
    """Test that GET /books/<id> returns 200 status code for existing book."""
    # First, add a book to the database
    response = client.post('/books', json={
        'title': 'Test Book',
        'authors': ['Test Author'],
        'description': 'A book for testing.',
        'cover_url': 'http://example.com/cover.jpg'
    })
    assert response.status_code == 201
    book_id = response.get_json()['id']
    
    # Now, retrieve the book by ID
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Book'
    assert 'Test Author' in data['author'] or 'Test Author' in data.get('authors', [])
    assert data.get('cover_url') == 'http://example.com/cover.jpg'

def test_post_book(client):
    """Test that POST /books returns 201 status code for a new book"""

