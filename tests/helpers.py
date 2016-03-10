import os

import pytest

from flask_forecaster.config import require

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

if pytest.config.getoption("--runslow"):
    TOKEN = require('VALID_API_TOKEN')
else:
    TOKEN = 'dummy token'
