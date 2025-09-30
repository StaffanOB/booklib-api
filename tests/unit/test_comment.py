import pytest
from app import create_app, db
from app.models import User, Book, Comment

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

def test_comment_model_creation(app):
    with app.app_context():
        user = User(username="commentuser", email="commentuser@example.com", password_hash="pw")
    book = Book(title="Comment Book")
    db.session.add(user)
    db.session.add(book)
    db.session.commit()
    comment = Comment(content="Unit test comment", book_id=book.id, user_id=user.id)
    db.session.add(comment)
    db.session.commit()
    fetched = Comment.query.filter_by(content="Unit test comment").first()
    assert fetched is not None
    assert fetched.book_id == book.id
    assert fetched.user_id == user.id
