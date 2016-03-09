import os

import pytest

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

TOKEN = os.getenv('VALID_API_TOKEN')
