#! /usr/bin/env python3
"""Launch the flask-forecaster application."""

import logging
import sys


logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s : %(name)s : %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger('launch_app')

if __name__ == '__main__':
    from flask_forecaster import app
    host, port = app.config['SERVER_BASE'], app.config['SERVER_PORT']
    logger.info('starting app on %s, %s', host, port)
    app.run(host=host, port=int(port))
