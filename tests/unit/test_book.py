import pytest
from app import create_app, db

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
def test_user_model_creation(app):
    from app import db
    from app.models import User
    with app.app_context():
        user = User(username="unituser", email="unituser@example.com", password_hash="hashedpw")
        db.session.add(user)
        db.session.commit()
        fetched = User.query.filter_by(username="unituser").first()
        assert fetched is not None
        assert fetched.email == "unituser@example.com"
        assert fetched.is_active is True

def test_tag_model_creation(app):
    from app import db
    from app.models import Tag
    with app.app_context():
        tag = Tag(name="unit-tag")
        db.session.add(tag)
        db.session.commit()
        fetched = Tag.query.filter_by(name="unit-tag").first()
        assert fetched is not None
        assert fetched.name == "unit-tag"

def test_comment_model_creation(app):
    from app import db
    from app.models import User, Book, Comment
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

def test_rating_model_creation(app):
    from app import db
    from app.models import User, Book, Rating
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

def test_plugin_model_creation(app):
    from app import db
    from app.models import Plugin
    with app.app_context():
        plugin = Plugin(name="unit-plugin", description="Unit test plugin.")
        db.session.add(plugin)
        db.session.commit()
        fetched = Plugin.query.filter_by(name="unit-plugin").first()
        assert fetched is not None
        assert fetched.description == "Unit test plugin."
        assert fetched.is_enabled is True

def test_book_full_info_returned(app):
    from app import db
    from app.models import Book
    with app.app_context():
        book = Book(
            title="Full Info Book",
            description="A book with all info",
            publish_year=2025,
            series="Unit Series",
            cover_url="http://example.com/cover.jpg"
        )
        db.session.add(book)
        db.session.commit()
        fetched = Book.query.filter_by(title="Full Info Book").first()
        assert fetched is not None
    assert fetched.title == "Full Info Book"
    assert fetched.description == "A book with all info"
    assert fetched.publish_year == 2025
    assert fetched.series == "Unit Series"
    assert fetched.cover_url == "http://example.com/cover.jpg"

def test_books_full_endpoint(client, app):
    from app import db
    from app.models import Book, User, Rating, Comment
    with app.app_context():
        # Create user, book, rating, comment
        user = User(username="fulluser", email="fulluser@example.com", password_hash="pw")
    book = Book(title="Full Endpoint Book", description="desc", publish_year=2025, series="Series", cover_url="http://example.com/cover.jpg")
    db.session.add(user)
    db.session.add(book)
    db.session.commit()
    rating = Rating(rating=4, book_id=book.id, user_id=user.id)
    comment = Comment(content="Great book!", book_id=book.id, user_id=user.id)
    db.session.add(rating)
    db.session.add(comment)
    db.session.commit()

    # Use test client to call endpoint
    response = client.get(f"/books/{book.id}/full")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == book.id
    assert data["title"] == "Full Endpoint Book"
    assert data["description"] == "desc"
    assert data["publish_year"] == 2025
    assert data["series"] == "Series"
    assert data["cover_url"] == "http://example.com/cover.jpg"
    assert data["average_rating"] == 4
    assert len(data["ratings"]) == 1
    assert data["ratings"][0]["rating"] == 4
    assert len(data["comments"]) == 1
    assert data["comments"][0]["content"] == "Great book!"
