# /root/tests/conftest.py

import pytest
from flask import Flask
from db import db as _db
from models import AuthorModel, BookModel, CategoryModel
from resources.category_list import blp as category_list_blp


@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['API_TITLE'] = 'Test API'
    app.config['API_VERSION'] = 'v1'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    _db.init_app(app)

    with app.app_context():
        _db.create_all()

    from flask_smorest import Api
    api = Api(app)
    api.register_blueprint(category_list_blp)

    yield app

    with app.app_context():
        _db.drop_all()

@pytest.fixture(scope='module')
def db(app):
    return _db

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(db):
    # Clear existing data to avoid duplicates
    db.session.query(BookModel).delete()
    db.session.query(CategoryModel).delete()
    db.session.query(AuthorModel).delete()

    # Add initial test data with unique names
    author = AuthorModel(name="Test Author")
    book = BookModel(title="Test Book", author=author)
    category = CategoryModel(name="Test Category")

    db.session.add(author)
    db.session.add(book)
    db.session.add(category)
    db.session.commit()


    yield db
    db.session.rollback()
    db.session.close()
