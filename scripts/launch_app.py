#! /usr/bin/env python3
"""Launch the flask-forecaster application."""
import os

from flask_forecaster import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))
