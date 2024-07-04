import pytest
from models import BookModel, AuthorModel, CategoryModel
from db import db

@pytest.fixture
def new_book():
    return {"title": "Test Book", "author_id": 1}

@pytest.fixture
def new_author():
    return {"name": "Test Author"}

@pytest.fixture
def new_category():
    return {"name": "Test Category"}

def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200

def test_create_book(client, new_book, new_author, new_category):
    client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)
    new_book["category_ids"] = [category_response.get_json()["id"]]
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == new_book["title"]

def test_get_book(client, new_book, new_author, new_category):
    client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)
    new_book["category_ids"] = [category_response.get_json()["id"]]
    response = client.post("/books", json=new_book)
    book_id = response.get_json()["id"]
    response = client.get(f"/book/{book_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == new_book["title"]

def test_update_book(client, new_book, new_author, new_category):
    client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)
    new_book["category_ids"] = [category_response.get_json()["id"]]
    response = client.post("/books", json=new_book)
    book_id = response.get_json()["id"]
    update_data = {"title": "Updated Book"}
    response = client.put(f"/book/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Book"

def test_delete_book(client, new_book, new_author, new_category):
    client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)
    new_book["category_ids"] = [category_response.get_json()["id"]]
    response = client.post("/books", json=new_book)
    book_id = response.get_json()["id"]
    response = client.delete(f"/book/{book_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Book deleted"
