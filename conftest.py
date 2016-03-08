import pytest

from flask_forecaster import APP as app_func

@pytest.fixture
def app():
    return app_func
