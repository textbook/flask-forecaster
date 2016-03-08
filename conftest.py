import pytest

from flask_forecaster import app as app_

@pytest.fixture
def app():
    return app_

def pytest_addoption(parser):
    parser.addoption(
        "--runslow",
        action="store_true",
        help="run slow tests"
    )
