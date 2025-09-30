import pytest
from app import create_app, db
from app.models import Tag

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

def test_tag_model_creation(app):
    with app.app_context():
        tag = Tag(name="unit-tag")
        db.session.add(tag)
        db.session.commit()
        fetched = Tag.query.filter_by(name="unit-tag").first()
        assert fetched is not None
        assert fetched.name == "unit-tag"
