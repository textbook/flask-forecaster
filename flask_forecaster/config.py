"""Flask configuration options."""

import os


class ConfigError(ValueError):
    """Specific error for configuration issues."""
    pass


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


class Config:
    """Configuration defaults."""

    DEBUG = False
    SECRET_KEY = 'youwillneverguessme'
    SERVER_NAME = 'localhost:5000'
    TESTING = False

    @classmethod
    def for_current_env(cls, env_var='FLASK_CONFIG', default='prod'):
        """Generate configuration for the current environment.

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

        """
        env = os.getenv(env_var, default)
        if env == 'dev':
            config_vars = dict(
                DEBUG=True,
            )
        elif env == 'prod':
            config_vars = dict(
                SECRET_KEY=require('FLASK_SECRET_KEY'),
                SERVER_NAME='0.0.0.0:{}'.format(require('PORT')),
            )
        elif env == 'test':
            config_vars = dict(
                VALID_TOKEN=require('VALID_API_TOKEN'),
                TESTING=True,
            )
        else:
            raise ValueError('unrecognised environment: {!r}'.format(env))
        config_vars['environment'] = env
        return type(env, (cls,), config_vars)
