import textwrap
from unittest import mock
from unittest.mock import call

import pytest

from flask_forecaster.config import Config, ConfigError, _parse_vcap, _require


@mock.patch('flask_forecaster.config.os.getenv')
def test_require_success(getenv):
    getenv.return_value = 'world'

    assert _require('hello') == 'world'
    getenv.assert_called_once_with('hello')


@mock.patch('flask_forecaster.config.os.getenv')
def test_require_failure(getenv):
    getenv.side_effect = ConfigError

    with pytest.raises(ConfigError):
        _require('hello')
    getenv.assert_called_once_with('hello')


@mock.patch('flask_forecaster.config.os.getenv')
class TestConfig:

    def test_unrecognised_env(self, getenv):
        getenv.return_value = 'garbage'
        with pytest.raises(ValueError):
            Config.for_current_env()

    def test_unsupplied_env(self, getenv):
        env = 'dev'
        getenv.return_value = env
        config = Config.for_current_env('hello')
        assert config.environment == env
        getenv.assert_any_call('hello', 'prod')

    def test_default_env(self, getenv):
        env = 'test'
        getenv.return_value = env
        config = Config.for_current_env('hello', 'world')
        assert config.environment == env
        getenv.assert_any_call('hello', 'world')

    @pytest.mark.parametrize('env,debug,testing,requires', [
        ('dev', True, False, []),
        ('test', False, True, ['VALID_API_TOKEN', 'ACCESSIBLE_PROJECT']),
        ('prod', False, False, ['FLASK_SECRET_KEY', 'PORT']),
    ])
    @mock.patch('flask_forecaster.config._require')
    @mock.patch('flask_forecaster.config._parse_vcap')
    def test_config_environment(self, _parse_vcap, _require, getenv, env, debug, testing, requires):
        getenv.side_effect = lambda env_var, default: default
        config = Config.for_current_env(default=env)
        assert config.DEBUG is debug
        assert config.TESTING is testing
        _require.assert_has_calls(
            [call(req) for req in requires],
            any_order=True,
        )
        if env == 'prod':
            # Production environments also access VCAP_SERVICES
            _parse_vcap.assert_called_once_with(
                'POSTGRES_SERVICE',
                (0, 'credentials', 'uri'),
            )


@mock.patch('flask_forecaster.config._require')
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

    result = _parse_vcap(
        'POSTGRES_SERVICE',
        (0, 'credentials', 'uri'),
    )

    assert result == 'postgres://somepath'
    _require.assert_any_call('VCAP_SERVICES')
    _require.assert_any_call('POSTGRES_SERVICE')
