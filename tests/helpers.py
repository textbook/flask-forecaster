import os

import pytest

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

status = type('HttpStatusCodes', (object,), dict(
    NOT_FOUND=404,
    REDIRECTED=302,
    OK=200,
))

TOKEN = os.getenv('VALID_API_TOKEN')
