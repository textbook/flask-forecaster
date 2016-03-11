"""Flask configuration options."""

import json
import logging
import os

logger = logging.getLogger(__name__)


class ConfigError(ValueError):
    """Specific error for configuration issues."""
    pass


class Config(object):
    """Configuration defaults."""

    DEBUG = False
    SECRET_KEY = 'youwillneverguessme'
    SERVER_BASE = 'localhost'
    SERVER_PORT = '5000'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/flask_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @classmethod
    def for_current_env(cls, env_var='FLASK_CONFIG', default='prod'):
        """Generate configuration for the current environment.

        Notes:
          There is a special case for the documentation, which is built
          and hosted on `ReadTheDocs`_.

        Arguments:
          env_var (:py:class:`str`, optional): The environment variable
            to get the current Flask environment from (defaults to
            ``'FLASK_CONFIG'``).
          default (:py:class:`str`, optional): The Flask environment to
            default to if ``env_var`` is not set (defaults to
            ``'prod'``).

        Returns:
          :py:class:`type`: A new :py:class:`Config` subclass with the
            appropriate attributes.

        Raises:
          :py:class:`ValueError`: If the Flask environment is not one
            of ``'dev'``, ``'prod'`` or ``'test'``.

        .. _ReadTheDocs:
          https://readthedocs.org/

        """
        if os.getenv('READTHEDOCS'):
            config = type('RTFD', (cls,), dict(SQLALCHEMY_DATABASE_URI=None))
            return config
        env = os.getenv(env_var, default)
        if env == 'dev':
            config_vars = dict(
                DEBUG=True,
            )
        elif env == 'prod':
            config_vars = dict(
                SQLALCHEMY_DATABASE_URI=parse_vcap(
                    'POSTGRES_SERVICE',
                    (0, 'credentials', 'uri'),
                ),
                SECRET_KEY=require('FLASK_SECRET_KEY'),
                SERVER_BASE='0.0.0.0',
                SERVER_PORT=require('PORT'),
            )
        elif env == 'test':
            config_vars = dict(
                PROJECT_ID=require('ACCESSIBLE_PROJECT'),
                VALID_TOKEN=require('VALID_API_TOKEN'),
                TESTING=True,
            )
        else:
            raise ValueError('unrecognised environment: {!r}'.format(env))
        config_vars['environment'] = env
        logger.info('configuring %r environment', env)
        return type(env, (cls,), config_vars)


def parse_vcap(service, route):
    """Extract service details from VCAP_SERVICES.

    Arguments:
      service (:py:class:`str`): The environment variable holding the
        name of the service.
      route (:py:class:`tuple`): The path to the value (list indices
        and dictionary keys).

    Returns:
      :py:class:`str`: The required configuration string.

    """
    data = json.loads(require('VCAP_SERVICES'))
    config = data.get(require(service))
    for key in route:
        config = config[key]
    return config


def require(name, env='prod'):
    """Require a specific environment variable to be present.

    Arguments:
      name (:py:class:`str`): The name of the environment variable.
      env (:py:class:`str`, optional): The configuration environment in
        which that variable is required (defaults to ``'prod'``).

    Returns:
      :py:class:`str`: The value of the environment variable.

    Raises:
      :py:class:`ConfigError`: If the variable is not present.

    """
    value = os.getenv(name)
    if value is None:
        raise ConfigError('{} is required in {} environments'.format(name, env))
    return value
