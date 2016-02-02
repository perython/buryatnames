# coding: utf-8

# Stdlib imports
import hashlib

# Core Flask imports
from itsdangerous import JSONWebSignatureSerializer as Serializer

# Third-party app imports
from flask.ext.login import UserMixin

# Imports from your apps
from init.flask_init import app
from init.database import db, TimestampMixin, BaseModel


class User(BaseModel, TimestampMixin, UserMixin, db.Model):
    __tablename__ = 'auth_user'

    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.Text, default='')
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def makepswd(password):
        secret = app.config['SECRET_KEY']
        return hashlib.md5(password.encode('utf-8').join(secret)).hexdigest()

    def maketoken(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'user_id': self.id})
        return token

    @property
    def is_active(self):
        return self.active
