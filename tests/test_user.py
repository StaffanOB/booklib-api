import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from app import create_app, db
from models import UserModel

@pytest.fixture
def app():
    app = create_app("sqlite:///:memory:")
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def register_test_user(client, username="test_user", password="testpassword", email="test@example.com"):
    user_data = {
        "username": username,
        "password": password,
        "email": email,
        "surname": "TestSurname",
        "firstname": "TestFirstname",
    }
    response = client.post('/register', json=user_data)
    assert response.status_code == 201


def login_test_user(client, username="test_user", password="testpassword"):
    user_data = {
        "username": username,
        "password": password,
    }
    response = client.post('/login', json=user_data)
    assert response.status_code == 200
    return response.json['access_token']


def test_register_user(client):
    register_test_user(client)


def test_login_user(client):
    register_test_user(client)
    login_test_user(client)


def test_jwt_authentication(client):
    register_test_user(client)
    login_test_user(client)

    access_token = login_test_user(client)

    # Make a request to a protected endpoint with the access token
    response = client.get('/user/1', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200  # Assuming the protected endpoint returns a 200 status code


# TODO: Fix refresh token tests  <02-02-24, Staffan > #
#def test_refresh_token(client):
#    register_test_user(client)
#    access_token = login_test_user(client)
#
#    response = client.post('/refresh', headers={"Authorization": f"Bearer {access_token}"})
#
#    assert response.status_code == 200
#    # Additional assertions can be added based on your application logic


def test_logout_user(client):
    register_test_user(client)
    access_token = login_test_user(client)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post('/logout', headers=headers)

    assert response.status_code == 200


def test_get_user(client):
    register_test_user(client)
    access_token = login_test_user(client)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get('/user/1', headers=headers)

    assert response.status_code == 200


def test_list_users(client):
    register_test_user(client, username="test_user1", email="test1@example.com")
    register_test_user(client, username="test_user2", email="test2@example.com")

    response = client.get('/users')

    assert response.status_code == 200
    assert len(response.json) == 2


def test_list_users_no_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 0


# TODO: Add user pagination tests <02-02-24, yourname> #
#def test_list_users_pagination(client):
#    # Create more than the default number of users
#    for i in range(10):
#        register_test_user(client, username=f"test_user{i}", email=f"test_{i}@example.com")
#
#    # Test pagination with a limit of 5 users per page
#    response_page1 = client.get('/users?limit=5&page=1')
#    response_page2 = client.get('/users?limit=5&page=2')
#
#    assert response_page1.status_code == 200
#    assert len(response_page1.json) == 5
#
#    assert response_page2.status_code == 200
#    assert len(response_page2.json) == 5
#
#
#def test_list_users_filter(client):
#    register_test_user(client, username="test_filtered_user", email="filtered@example.com")
#
#    # Test filtering by username
#    response = client.get('/users?filter=user')
#    assert response.status_code == 200
#    assert len(response.json) == 1
#
#    # Test filtering by email
#    response = client.get('/users?filter=filtered@example.com')
#    assert response.status_code == 200
#    assert len(response.json) == 1
