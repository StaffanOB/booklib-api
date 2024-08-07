import pytest
from models import CategoryModel
from db import db


@pytest.fixture
def new_category():
    return {"name": "Test Category"}


def test_get_categories(client):
    response = client.get("/categories")
    assert response.status_code == 200


def test_create_category(client, new_category):
    response = client.post("/categories", json=new_category)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == new_category["name"]


def test_get_category(client, new_category):
    response = client.post("/categories", json=new_category)
    category_id = response.get_json()["id"]
    response = client.get(f"/category/{category_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == new_category["name"]


def test_update_category(client, new_category):
    response = client.post("/categories", json=new_category)
    category_id = response.get_json()["id"]
    update_data = {"name": "Updated Category"}
    response = client.put(f"/category/{category_id}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Category"


def test_delete_category(client, new_category):
    response = client.post("/categories", json=new_category)
    category_id = response.get_json()["id"]
    response = client.delete(f"/category/{category_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Category deleted"
