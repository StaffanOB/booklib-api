import pytest
from app import create_app
from flask import Flask
from db import db as _db
from models import AuthorModel, BookModel, CategoryModel
from resources.category_list import blp as category_list_blp


@pytest.fixture
def app():
    app = create_app("sqlite:///:memory:")
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            _db.create_all()
        yield client
