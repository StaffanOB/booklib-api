from models import BookModel


def test_get_books(test_client):
    response = test_client.get('/books')
    assert response.status_code == 200
    assert response.json() == []
