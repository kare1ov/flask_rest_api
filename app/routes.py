from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
import jwt

from . import app
from . import api
from . import db
from . import models
from . import schemas


post_schema = schemas.PostSchema()
user_schema = schemas.UserSchema()


class PostListApi(Resource):
    def get(self):
        posts = db.session.query(models.Post).all()
        return post_schema.dump(posts, many=True)

    def post(self):
        token = request.headers.get("X-Api-Key", "")
        if not token:
            return "", 401, {"WWW-Authenticate": "Basic realm='Auth required'"}
        try:
            uuid = jwt.decode(token, app.config["SECRET_KYE"])["user_id"]
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": "Basic realm='Auth required'"}
        user = db.session.query(models.User).filter_by(uuid=uuid).first()
        if not user:
            return "", 401, {"WWW-Authenticate": "Basic realm='Auth required'"}

        try:
            post = post_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post), 201


class PostApi(Resource):
    def get(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        return post_schema.dump(post)

    def put(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        post = post_schema.load(request.json, instance=post, session=db.session)
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)

    def delete(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        db.session.delete(post)
        db.session.commit()
        return "", 204


class UserListApi(Resource):
    def post(self):
        try:
            user = user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            return {"message": str(e)}, 409
        return user_schema.dump(user)


api.add_resource(PostListApi, "/posts")
api.add_resource(PostApi, "/posts/<uuid>")
api.add_resource(UserListApi, "/users")
