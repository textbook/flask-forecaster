"""The main web application."""

from flask import Flask, render_template

from .forms import TrackerApiForm


SECRET_KEY = 'somethingyoucantguess'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=('GET', 'POST'))
def home():
    """Basic home page."""
    form = TrackerApiForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)
