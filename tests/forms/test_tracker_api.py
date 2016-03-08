from flask_forecaster.forms import TrackerApiForm

def test_token_field(app):
    form = TrackerApiForm()
    assert getattr(form, 'token') is not None

def test_token_field_required(app):
    form = TrackerApiForm()
    form.validate()
    assert 'API token must be provided' in form.token.errors
