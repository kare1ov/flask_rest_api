import datetime
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt

from . import app
from . import db
from . import models


@app.route("/login")
def login():
    auth = request.authorization
    if not auth:
        return "", 401, {"WWW-Authenticate": "Basic realm='Auth required'"}
    user = db.session.query(models.User).filter_by(login=auth.get("username", "")).first()
    if user is None or not check_password_hash(user.password, auth.get("password", "")):
        return "", 401, {"WWW-Authenticate": "Basic realm='Auth required'"}
    token = jwt.encode(
        {
            "user_id": user.uuid,
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
        }, app.config["SECRET_KEY"]
    )
    return jsonify({"token": token.decode("utf-8")})
