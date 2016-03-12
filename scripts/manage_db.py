"""Database management and migration functionality."""

import logging
import sys

# pylint: disable=no-name-in-module,import-error
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
# pylint: enable=no-name-in-module,import-error

from flask_forecaster.flask_app import app, db

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s : %(name)s : %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger('manage_db')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    logger.info('managing the database')
    manager.run()
