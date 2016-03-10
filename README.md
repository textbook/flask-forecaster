# flask-forecaster

[![Build Status][1]][2]
[![Coverage Status][3]][4]

A Flask-based web app for forecasting Pivotal Tracker projects.

## Configuration

The current configuration supports three distinct environments, which
can be selected using the environment variable `FLASK_CONFIG`:

 * `dev`: For local development, which starts the app in debug mode;
 * `test`: For CI environments (e.g. Travis CI), which starts the app in 
 testing mode; and
 * `prod`: For production environments (e.g. Cloud Foundry), which 
 starts the app in its default mode and also requires:
     * `FLASK_SECRET_KEY`: The secret key for CORS protection.

Whenever `py.test` is run with the `--runslow` option (which is used by
default for `python setup.py test`), a valid Tracker API key must be 
provided as `VALID_API_TOKEN` for the integration testing.

In addition, for automatic deployment from Travis to Cloud Foundry, the 
following environment variables are required: `CF_ORG`; `CF_SPACE`; 
`CF_USERNAME`; and `CF_PASSWORD`.

  [1]: https://travis-ci.org/textbook/flask-forecaster.svg?branch=master
  [2]: https://travis-ci.org/textbook/flask-forecaster
  [3]: https://coveralls.io/repos/github/textbook/flask-forecaster/badge.svg?branch=master
  [4]: https://coveralls.io/github/textbook/flask-forecaster?branch=master
