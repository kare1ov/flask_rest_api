import json
from unittest import mock

from app import app


def test_create_post():
    with mock.patch("app.db.session.add") as add, \
            mock.patch("app.db.session.commit") as commit:
        r = app.test_client().post("/posts", data=json.dumps(
            {
                "title": "Title1",
                "body": "ergwe",
                "date": "2020-04-01T00:00"
            }
        ), content_type="application/json")
        add.assert_called_once()
        commit.assert_called_once()
    assert r.status_code == 201
    assert r.json["title"] == "Title1"
