import pytest
from models import CategoryModel
from db import db

def test_get_book_categories(client, new_book):
    response = client.get(f"/books/{new_book.id}/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1  # Assuming the new book has 1 category linked to it

def test_add_category_to_book(client, new_book, new_category, db):
    new_category = CategoryModel(name="New Category")
    db.session.add(new_category)
    db.session.commit()

    response = client.put(f"/books/{new_book.id}/categories", json={"category_id": new_category.id})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2  # Now the book should have 2 categories


def test_remove_category_from_book(client, new_book, new_category):
    response = client.delete(f"/books/{new_book.id}/categories", json={"category_id": new_category.id})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0  # Now the book should have no categories
