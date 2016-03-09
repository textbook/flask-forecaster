"""The main web application."""
import os

from flask import Flask, render_template

from .forms import TrackerApiForm
from .tracker import Tracker


SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'somethingyoucantguess'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=('GET', 'POST'))
def home():
    """Basic home page."""
    form = TrackerApiForm()
    if form.validate_on_submit():
        projects = Tracker.validate_token(form.token.data)
        if projects:
            return render_template('index.html', projects=projects)
        form.token.errors = ['API token invalid']
    return render_template('index.html', form=form)
