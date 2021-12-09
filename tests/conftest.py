from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.config import config
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
from app.main import app

pg_cfg: dict = config.dict()["POSTGRESQL_SETTINGS"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{pg_cfg['USERNAME']}:{pg_cfg['PASSWORD']}@{pg_cfg['HOST']}/{pg_cfg['DATABASE']}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("Session fixture run")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "jatin@example.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {"email": "netu@example.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":  f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    post_data = [{"title": "1 title", "content": "1 content", "owner_id": test_user['id']},
                 {"title": "2 title", "content": "2 content", "owner_id": test_user['id']},
                 {"title": "3 title", "content": "3 content", "owner_id": test_user['id']},
                 {"title": "4 title", "content": "4 content", "owner_id": test_user2['id']}]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, post_data))
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()
