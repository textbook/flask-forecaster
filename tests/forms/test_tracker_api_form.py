import pytest

from flask_forecaster.forms import TrackerApiForm


@pytest.mark.parametrize('input_data,expected_errors', [
    (None, ['API token must be provided']),
    ('abc123', ['API token must be 32 alphanumeric characters']),
    ('abc1' * 8, []),
])
def test_token_field(app, input_data, expected_errors):
    form = TrackerApiForm()
    form.token.raw_data = input_data
    form.token.data = input_data
    form.validate()
    assert form.token.errors == expected_errors
