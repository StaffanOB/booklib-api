from flask_smorest.spec.plugins import re
from marshmallow import Schema, fields
from sqlalchemy.orm import load_only


class PlainBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)


class BookSchema(PlainBookSchema):
    author_ids = fields.List(fields.Int(), load_only=True)
    authors = fields.List(fields.Nested("PlainAuthorSchema"), dump_only=True)
    category_ids = fields.List(fields.Int(), load_only=True)
    categories = fields.List(fields.Nested(
        "PlainCategorySchema"), dump_only=True)


class BookCreateSchema(Schema):
    title = fields.String(required=True, description="Title of the book")
    author_names = fields.List(
        fields.String(), required=True, description="List of author names")
    category_names = fields.List(
        fields.String(), required=True, description="List of category names")


class BookUpdateSchema(Schema):
    title = fields.Str()
    author_id = fields.Int()
    category_ids = fields.List(fields.Int(), load_only=True)


class PlainAuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class AuthorSchema(PlainAuthorSchema):
    books = fields.List(fields.Nested(PlainBookSchema), dump_only=True)


class AuthorUpdateSchema(Schema):
    name = fields.Str()


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class CategorySchema(PlainCategorySchema):
    books = fields.List(fields.Nested(PlainBookSchema), dump_only=True)


class CategoryUpdateSchema(Schema):
    name = fields.Str()


class BookCategorySchema(Schema):
    category_id = fields.Int(required=True)


class UserSchema(Schema):
    """
    User Schema
        id: dump only
        username: id required
        password: is only loded newver sent
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    surname = fields.Str(required=False)
    firstname = fields.Str(required=False)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)


class PlainMemberSchema(Schema):
    mid = fields.Int(dump_only=True)


class MemberSchema(PlainMemberSchema):
    uid = fields.Int(required=True, load_only=True)
    user = fields.Nested(UserSchema(), dump_only=True)
    surname = fields.Str(required=False)
    firstname = fields.Str(required=False)
