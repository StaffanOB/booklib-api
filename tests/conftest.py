import pytest
from flask import Flask
from db import db as _db
from models import BookModel, CategoryModel, BookCategoryModel, AuthorModel


@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    _db.init_app(app)

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='module')
def db(app):
    return _db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(db):
    #    author = AuthorModel(name='Test Author 1')
    #    db.session.add(author)
    #    db.session.commit()

    book = BookModel(title='Test Book 1', author_id=author.id)
    db.session.add(book)
    db.session.commit()

    category = CategoryModel(name='Test Category 1')
    db.session.add(category)
    db.session.commit()

    book_category = BookCategoryModel(book_id=book.id, category_id=category.id)
    db.session.add(book_category)
    db.session.commit()
    yield db
    db.session.rollback()
    db.session.close()
