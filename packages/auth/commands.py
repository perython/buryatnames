# coding: utf-8

# Stdlib imports

# Core Flask imports

# Third-party app imports
from flask.ext.script import Command

# Imports from your apps
from init.database import db
from .models import User


class AddUser(Command):
    def run(self):
        while True:
            email = raw_input('email: ')
            password = raw_input('password: ')

            email = email.strip()
            if User.query.filter(User.email == email).count():
                print 'User with email {} already exists'.format(email)
            else:
                break

        user = User(email=email)
        user.password = user.makepswd(password)
        db.session.add(user)
        db.session.commit()
