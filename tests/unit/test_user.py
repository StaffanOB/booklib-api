import pytest
from app import create_app, db
from app.models import User

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

def test_user_model_creation(app):
    with app.app_context():
        user = User(username="unituser", email="unituser@example.com", password_hash="hashedpw")
        db.session.add(user)
        db.session.commit()
        fetched = User.query.filter_by(username="unituser").first()
        assert fetched is not None
        assert fetched.email == "unituser@example.com"
        assert fetched.is_active is True
