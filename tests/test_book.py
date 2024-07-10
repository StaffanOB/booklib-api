import pytest
import pprint
from app import create_app, db
from models import AuthorModel, CategoryModel, BookModel


@pytest.fixture
def new_author():
    return {"name": "Author Name"}


@pytest.fixture
def new_category():
    return {"name": "Category Name"}


@pytest.fixture
def new_book():
    return {"title": "Book Title", "category_ids": [], "author_ids": None}


def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200


def test_create_book(client, new_book, new_author, new_category):
    author_response = client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)

    # Use the id from the response to update the new_book dictionary
    new_book["category_ids"] = [category_response.get_json()["id"]]
    new_book["author_ids"] = [author_response.get_json()["id"]]

    # Post the new book
    response = client.post("/books", json=new_book)
    assert response.status_code == 201

    response = client.get("/books")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == new_book["title"]


# def test_get_books(client, new_book, new_author, new_category):
#     client.post("/authors", json=new_author)
#     category_response = client.post("/categories", json=new_category)
#     new_book["category_ids"] = [category_response.get_json()["id"]]
#     response = client.post("/books", json=new_book)
#     assert response.status_code == 201
#
#     response = client.get("/books")
#     assert response.status_code == 200
#     data = response.get_json()
#     assert len(data) == 1
#     assert data[0]["title"] == new_book["title"]
#
#     # def test_update_book(client, new_book, new_author, new_category):
#    client.post("/authors", json=new_author)
#    category_response = client.post("/categories", json=new_category)
#    new_book["category_ids"] = [category_response.get_json()["id"]]
#    response = client.post("/books", json=new_book)
#    book_id = response.get_json()["id"]
#
#    update_data = {"title": "Updated Book"}
#    response = client.put(f"/book/{book_id}", json=update_data)
#    assert response.status_code == 200
#    data = response.get_json()
#    assert data["title"] == "Updated Book"
#
#
# def test_delete_book(client, new_book, new_author, new_category):
#    client.post("/authors", json=new_author)
#    category_response = client.post("/categories", json=new_category)
#    new_book["category_ids"] = [category_response.get_json()["id"]]
#    response = client.post("/books", json=new_book)
#    book_id = response.get_json()["id"]
#
#    response = client.delete(f"/book/{book_id}")
#    assert response.status_code == 200
#    data = response.get_json()
#    assert data["message"] == "Book deleted"
