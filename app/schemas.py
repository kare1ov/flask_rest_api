from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import models


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Post
        exclude = "id",
        load_instance = True



class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        exclude = "id",
        load_instance = True
