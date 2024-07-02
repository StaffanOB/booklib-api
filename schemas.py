from flask_smorest.spec.plugins import re
from marshmallow import Schema, fields
from sqlalchemy.orm import load_only


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class BookSchema(PlainBookSchema):
    author = fields.Str(required=True)


class BookUpdateSchema(Schema):
    title = fields.Str()
    author = fields.Str()


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.Nested(PlainItemSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


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
