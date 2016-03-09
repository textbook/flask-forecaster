"""A Flask-based web app for forecasting Pivotal Tracker projects."""

import logging

from .flask_app import app

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.3'

logging.getLogger(__name__).addHandler(logging.NullHandler())
