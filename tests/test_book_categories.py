from flask import url_for


def test_get_book_categories(client):
    response = client.get(url_for('/book/1/categories'))
    assert response.status_code == 200
    assert len(response.json) == 0


def test_post_book_category(client):
    response = client.post(url_for('/book/1/categories'),
                           json={'category_id': 1})
    assert response.status_code == 201
    assert response.json['name'] == 'Test Category 1'


def test_put_book_category(client):
    response = client.put('/book/1/categories',
                          json={'id': 1, 'is_primary': True})
    assert response.status_code == 200
    assert response.json['name'] == 'Test Category 1'


def test_delete_book_category(client):
    client.post(url_for('/book/1/categories', json={'category_id': 1}))
    response = client.delete(url_for('/book/1/categories/1'))
    assert response.status_code == 200
    assert response.josn['message'] == 'Category deleted'
