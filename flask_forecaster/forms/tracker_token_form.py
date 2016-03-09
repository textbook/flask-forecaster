"""Forms for interaction with the Tracker API."""

from flask_wtf import Form
from wtforms import StringField, validators

class TrackerApiForm(Form):
    """Allow the user to input their Tracker API token."""

    token = StringField('Enter Tracker API token:', validators=[
        validators.InputRequired(
            message='API token must be provided'
        ),
        validators.Regexp(
            r'[a-z\d]{32}',
            message='API token must be 32 alphanumeric characters',
        )
    ])
