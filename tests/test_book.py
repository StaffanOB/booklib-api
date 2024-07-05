import pytest
from app import create_app, db
from models import AuthorModel, CategoryModel, BookModel
@pytest.fixture(scope='session')
def app():
    app = create_app("sqlite:///:memory:")
    return app

@pytest.fixture(scope='session')
def client(app, app_context):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200


    # def test_get_books(client, new_book, new_author, new_category):
    #    client.post("/authors", json=new_author)
    #    category_response = client.post("/categories", json=new_category)
    #    new_book["category_ids"] = [category_response.get_json()["id"]]
    #    response = client.post("/books", json=new_book)
    #    assert response.status_code == 201
    #
    #    response = client.get("/books")
    #    assert response.status_code == 200
    #    data = response.get_json()
    #    assert len(data) == 1
    #    assert data[0]["title"] == new_book["title"]
    #
    #
    # def test_update_book(client, new_book, new_author, new_category):
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
