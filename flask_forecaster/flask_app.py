"""The main web application."""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    """Basic home page."""
    return 'hello world'
