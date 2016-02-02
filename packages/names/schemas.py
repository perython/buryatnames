# coding: utf-8

# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import Schema, fields

# Imports from your apps


__all__ = (
    'NameSchema',
    'NamesSchema',
    'CategorySchema',
)


class NameSchema(Schema):
    id = fields.Int(dump_only=True)
    author = fields.Str()
    title = fields.Str()
    desc = fields.Str()
    notes = fields.Str()
    cover_url = fields.Str()
    status = fields.Int()
    finished_at = fields.DateTime(format='iso')
    created_at = fields.DateTime(format='iso')


class NamesSchema(Schema):
    page = fields.Int()
    total = fields.Int()
    items = fields.Nested(NameSchema, many=True)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
