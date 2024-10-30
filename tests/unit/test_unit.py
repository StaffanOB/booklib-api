def test_get_books_returns_200(client):
    response = client.get('/books')
    assert response.status_code == 200


def test_get_books_returns_empty_list_when_no_books_exist(client):
    response = client.get('/books')
    assert response.json() == []


def test_get_books_returns_list_of_books(client, new_book, new_author, new_category):
    client.post("/authors", json=new_author)
    category_response = client.post("/categories", json=new_category)
    new_book["category_ids"] = [category_response.get_json()["id"]]
    client.post("/books", json=new_book)

    response = client.get('/books')
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == new_book["title"]