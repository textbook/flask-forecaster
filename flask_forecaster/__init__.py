"""A Flask-based web app for forecasting Pivotal Tracker projects."""

import logging

from .flask_app import app, __version__

__author__ = 'Jonathan Sharpe'

logging.getLogger(__name__).addHandler(logging.NullHandler())
