#! /usr/bin/env python3
"""Launch the flask-forecaster application."""
import os
import sys

from flask_forecaster import app

if __name__ == '__main__':
    app.run(
        debug='debug' in sys.argv,
        host='0.0.0.0',
        port=int(os.getenv('PORT') or 5000)
    )
