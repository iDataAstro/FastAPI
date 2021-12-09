import pytest
from jose import jwt
from app import schemas
from app.config import config

auth_cfg = config.dict()['AUTH2_SETTINGS']

def test_root_path(client):
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "yug@example.com", "password": "pass123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "yug@example.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, auth_cfg['SECRET_KEY'], auth_cfg['ALGORITHM'])
    id = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("noname@gmail.com", "mypass", 403),
    ("yug@example.com", "mypass", 403),
    ("noname@gmail.com", "pass123", 403),
    (None, "pass123", 422),
    ("yug@example.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
