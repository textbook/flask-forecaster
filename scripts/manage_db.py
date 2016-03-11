"""Database management and migration functionality."""

# pylint: disable=no-name-in-module,import-error
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
# pylint: enable=no-name-in-module,import-error

from flask_forecaster.flask_app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
