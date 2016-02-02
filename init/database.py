# coding: utf-8

# Stdlib imports
from datetime import datetime

# Core Flask imports

# Third-party app imports
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

# Imports from your apps


db = SQLAlchemy()


class BaseModel(object):
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
