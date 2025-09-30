import pytest
from app import create_app, db
from app.models import Plugin

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

def test_plugin_model_creation(app):
    with app.app_context():
        plugin = Plugin(name="unit-plugin", description="Unit test plugin.")
        db.session.add(plugin)
        db.session.commit()
        fetched = Plugin.query.filter_by(name="unit-plugin").first()
        assert fetched is not None
        assert fetched.description == "Unit test plugin."
        assert fetched.is_enabled is True
