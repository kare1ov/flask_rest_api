import uuid
from werkzeug.security import generate_password_hash

from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(95))
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password = generate_password_hash(password)
        self.uuid = str(uuid.uuid4())


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, title, body, date):
        self.title = title
        self.body = body
        self.date = date
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}', '{self.uuid}')"
