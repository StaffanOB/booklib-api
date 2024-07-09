import pytest
from app import app


@pytest.fixture
def test_user_1():
    return {
        "username": "test_user",
        "password": "testpassword",
        "email": "test_user_1@example.com",
        "surname": "TestSurname",
        "firstname": "TestFirstname",
    }


@pytest.fixture
def test_user_2():
    return {
        "username": "test_user_2",
        "password": "testpassword",
        "email": "test_user_2@example.com",
        "surname": "TestSurname",
        "firstname": "TestFirstname",
    }


def register_test_user(client, username="test_user", password="testpassword", email="test@example.com"):
    user_data = {
        "username": username,
        "password": password,
        "email": email,
        "surname": "surname",
        "firstname": "firstname",
    }
    response = client.post('/register', json=user_data)
    assert response.status_code == 201


def login_test_user(client, test_user_1):
    user_data = {
        "username": test_user_1['username'],
        "password": test_user_1['password'],
    }
    response = client.post('/login', json=user_data)
    assert response.status_code == 200
    return response.json['access_token']


def test_register_user(client):
    register_test_user(client)


def test_login_user(client, test_user_1):
    register_test_user(client)
    login_test_user(client, test_user_1)


def test_jwt_authentication(client, test_user_1):
    register_test_user(client)
    login_test_user(client, test_user_1)

    access_token = login_test_user(client, test_user_1)

    # Make a request to a protected endpoint with the access token
    response = client.get(
        '/user/1', headers={"Authorization": f"Bearer {access_token}"})
    # Assuming the protected endpoint returns a 200 status code
    assert response.status_code == 200


def test_logout_user(client, test_user_1):
    register_test_user(client)
    access_token = login_test_user(client, test_user_1)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post('/logout', headers=headers)

    assert response.status_code == 200


def test_get_user(client, test_user_1):
    register_test_user(client)
    access_token = login_test_user(client, test_user_1)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get('/user/1', headers=headers)

    assert response.status_code == 200


def test_list_users(client, test_user_1, test_user_2):

    register_test_user(
        client, username=test_user_1['username'],
        email=test_user_1['email'])
    register_test_user(
        client, username=test_user_2['username'],
        email=test_user_2['email'])

    response = client.get('/users')

    assert response.status_code == 200
    assert len(response.json) == 2


def test_list_users_no_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 0
