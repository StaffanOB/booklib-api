import pytest
from flask import url_for
from db import db as _db
import models
from resources.category import blp as category_blp


def test_get_categories(client, init_database):
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Test Category 1"


def test_post_category(client, init_database):
    response = client.post("/categories", json={"name": "Test Category 2"})
    assert response.status_code == 201
    assert response.json["name"] == "Test Category 2"
