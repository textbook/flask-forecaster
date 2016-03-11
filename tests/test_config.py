import textwrap
from unittest import mock
from unittest.mock import call

import pytest

from flask_forecaster.config import Config, ConfigError, parse_vcap, require


@mock.patch('flask_forecaster.config.os.getenv')
def test_require_success(getenv):
    getenv.return_value = 'world'

    assert require('hello') == 'world'
    getenv.assert_called_once_with('hello')


@mock.patch('flask_forecaster.config.os.getenv')
def test_require_failure(getenv):
    getenv.side_effect = ConfigError

    with pytest.raises(ConfigError):
        require('hello')
    getenv.assert_called_once_with('hello')


@mock.patch('flask_forecaster.config.os.getenv')
class TestConfig:

    def test_unrecognised_env(self, getenv):
        getenv.side_effect = ['', 'garbage', '', '']
        with pytest.raises(ValueError):
            Config.for_current_env()

    def test_unsupplied_env(self, getenv):
        env = 'dev'
        getenv.side_effect = ['', env, '', '']
        config = Config.for_current_env('hello')
        assert config.environment == env
        getenv.assert_any_call('hello', 'prod')

    def test_default_env(self, getenv):
        env = 'test'
        getenv.side_effect = ['', env, '', '']
        config = Config.for_current_env('hello', 'world')
        assert config.environment == env
        getenv.assert_any_call('hello', 'world')

    def test_config_rtfd(self, getenv):
        getenv.return_value = 'foo'
        config = Config.for_current_env('hello', 'world')
        assert config.SQLALCHEMY_DATABASE_URI is None
        getenv.assert_any_call('READTHEDOCS')

    @pytest.mark.parametrize('env,debug,testing,requires', [
        ('dev', True, False, []),
        ('test', False, True, ['VALID_API_TOKEN', 'ACCESSIBLE_PROJECT']),
        ('prod', False, False, ['FLASK_SECRET_KEY', 'PORT']),
    ])
    @mock.patch('flask_forecaster.config.require')
    @mock.patch('flask_forecaster.config.parse_vcap')
    def test_config_environment(self, parse_vcap, require, getenv, env, debug, testing, requires):
        getenv.side_effect = lambda env_var, default=None: default
        config = Config.for_current_env(default=env)
        assert config.DEBUG is debug
        assert config.TESTING is testing
        require.assert_has_calls(
            [call(req) for req in requires],
            any_order=True,
        )
        if env == 'prod':
            # Production environments also access VCAP_SERVICES
            parse_vcap.assert_called_once_with(
                'POSTGRES_SERVICE',
                (0, 'credentials', 'uri'),
            )


@mock.patch('flask_forecaster.config.require')
def test_parse_vcap(_require):
    required = dict(
        VCAP_SERVICES=textwrap.dedent(
            """
            {
              "elephantsql-dev": [
              {
                "name": "elephantsql-dev-c6c60",
                "label": "elephantsql-dev",
                "plan": "turtle",
                "credentials": {
                  "uri": "postgres://somepath"
                }
              }
              ]
            }
            """
        ),
        POSTGRES_SERVICE='elephantsql-dev',
    )
    _require.side_effect = lambda name: required[name]

    result = parse_vcap(
        'POSTGRES_SERVICE',
        (0, 'credentials', 'uri'),
    )

    assert result == 'postgres://somepath'
    _require.assert_any_call('VCAP_SERVICES')
    _require.assert_any_call('POSTGRES_SERVICE')
