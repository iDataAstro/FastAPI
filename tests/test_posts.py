import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts = list(map(validate, res.json()))
    assert len(posts) == len(test_posts)
    assert res.status_code == 200
