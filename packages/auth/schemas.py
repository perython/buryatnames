# coding: utf-8

# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import Schema, fields

# Imports from your apps


__all__ = (
    'UserSchema',
    'UserLoginSchema',
)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
