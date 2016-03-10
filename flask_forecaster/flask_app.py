"""The main web application."""

import logging
import os

from flask import Flask, redirect, render_template, session, url_for

from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .forms import TrackerApiForm
from .tracker import Tracker

CONFIG_OPTIONS = dict(
    dev=DevelopmentConfig(),
    prod=ProductionConfig(),
    test=TestingConfig(),
)

logger = logging.getLogger(__name__)

__version__ = '0.0.3'

app = Flask(__name__)
app.config.from_object(CONFIG_OPTIONS[os.getenv('FLASK_CONFIG', 'prod')])


@app.route('/', methods=('GET', 'POST'))
def home():
    """Basic home page."""
    form = TrackerApiForm()
    if 'token' in session:
        form.token.raw_data = session['token']
        form.token.data = session['token']
    if form.validate_on_submit():
        token = form.token.data
        logger.info('validating token %s', token)
        projects = Tracker.validate_token(token)
        if projects:
            session['token'] = token
            return render_template(
                'index.html',
                form=form,
                projects=projects,
                version=__version__,
            )
        form.token.errors = ['API token must be valid for the Tracker API']
    return render_template('index.html', form=form, version=__version__)


@app.route('/project/<int:project_id>')
def project(project_id):
    """Project details page."""
    token = session.get('token')
    if token is None:
        return redirect(url_for('home'))
    api = Tracker(token)
    return render_template('project.html', project=api.get_project(project_id))
