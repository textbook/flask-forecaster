#! /usr/bin/env python3
"""Launch the flask-forecaster application."""

import logging
import sys


logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.INFO,
    stream=sys.stdout,
)

if __name__ == '__main__':
    from flask_forecaster import app
    app.run()
