#! /usr/bin/env python3
"""Launch the flask-forecaster application."""
import logging
import os
import sys

from flask_forecaster import app

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.INFO,
    stream=sys.stdout,
)

if __name__ == '__main__':
    app.run(
        debug='debug' in sys.argv,
        host='0.0.0.0',
        port=int(os.getenv('PORT') or 5000)
    )
