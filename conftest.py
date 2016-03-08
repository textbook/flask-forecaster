import pytest

from flask_forecaster import app as app_

@pytest.fixture
def app():
    return app_
