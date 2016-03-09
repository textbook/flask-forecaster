"""The main web application."""

import logging
import os

from flask import Flask, render_template

from .forms import TrackerApiForm
from .tracker import Tracker

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'somethingyoucantguess'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=('GET', 'POST'))
def home():
    """Basic home page."""
    form = TrackerApiForm()
    if form.validate_on_submit():
        token = form.token.data
        logger.info('validating token %s', token)
        projects = Tracker.validate_token(token)
        if projects:
            return render_template('index.html', projects=projects)
        form.token.errors = ['API token must be valid for the Tracker API']
    return render_template('index.html', form=form)
