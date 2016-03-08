"""The main web application."""

from flask import Flask

APP = Flask(__name__)

@APP.route('/')
def home():
    """Basic home page."""
    return 'hello world'
