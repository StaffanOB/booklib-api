import pytest


def test_app_creation(client):
    response = client.get('/')
    assert response.status_code == 404  # The root URL should return a 404
