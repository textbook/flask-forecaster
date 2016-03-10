from unittest import mock
from unittest.mock import call

import pytest

from flask_forecaster.config import require, ConfigError, Config


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

    def test_development_environment(self, getenv):
        getenv.side_effect = lambda env_var, default: default
        config = Config.for_current_env(default='dev')
        assert config.DEBUG
        assert not config.TESTING

    @mock.patch('flask_forecaster.config.require')
    def test_testing_environment(self, require, getenv):
        getenv.side_effect = lambda env_var, default: default
        config = Config.for_current_env(default='test')
        assert not config.DEBUG
        assert config.TESTING
        require.assert_called_once_with('VALID_API_TOKEN')

    @mock.patch('flask_forecaster.config.require')
    def test_production_environment(self, require, getenv):
        getenv.side_effect = lambda env_var, default: default
        config = Config.for_current_env()
        assert not config.DEBUG
        assert not config.TESTING
        require.assert_has_calls(
            [call('FLASK_SECRET_KEY'), call('PORT')],
            any_order=True,
        )
