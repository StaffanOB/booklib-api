import pytest
from app import create_app, db
from app.models import User, Book, Rating

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

def test_rating_model_creation(app):
    with app.app_context():
        user = User(username="ratinguser", email="ratinguser@example.com", password_hash="pw")
    book = Book(title="Rating Book")
    db.session.add(user)
    db.session.add(book)
    db.session.commit()
    rating = Rating(rating=5, book_id=book.id, user_id=user.id)
    db.session.add(rating)
    db.session.commit()
    fetched = Rating.query.filter_by(rating=5).first()
    assert fetched is not None
    assert fetched.book_id == book.id
    assert fetched.user_id == user.id
    assert fetched.rating == 5
