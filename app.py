# coding: utf-8

# Stdlib imports
import os

# Core Flask imports
from flask import url_for
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Third-party app imports
from flask_cors import CORS

# Imports from your apps
from init.flask_init import app
from init.database import db
from init.login_manager_init import lm

app.config.from_envvar('BURYATNAMES_SETTINGS')
app.config['CORS_HEADERS'] = 'X-Requested-With, Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
cors = CORS(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def init():
    from packages.auth.views import auth
    from packages.auth.commands import AddUser
    app.register_blueprint(auth)
    manager.add_command('add_user', AddUser)

    from packages.names.views import names
    from packages.names.commands import AddNames
    app.register_blueprint(names)
    manager.add_command('add_names', AddNames)


db.init_app(app)
lm.init_app(app)
init()


with app.app_context():
    db.engine.dialect.supports_sane_rowcount = False
    db.engine.dialect.supports_sane_multi_rowcount = False


if __name__ == '__main__':
    manager.run()
