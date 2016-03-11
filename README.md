# flask-forecaster

[![Build Status][1]][2]
[![Coverage Status][3]][4]
[![Documentation Status][5]][6]

A Flask-based web app for forecasting Pivotal Tracker projects.

## Configuration

The current configuration supports three distinct environments, which
can be selected using the environment variable `FLASK_CONFIG`:

 * `dev`: For local development, which starts the app in debug mode;
 * `test`: For testing and continuous integration environments (e.g. 
 Travis CI), which starts the app in testing mode and also requires:
     * `ACCESSIBLE_PROJECT`: A project accessible using the supplied API
     token; and
     * `VALID_API_TOKEN`: A valid token for integration testing; and
 * `prod` [**default**]: For production environments (e.g. Cloud 
 Foundry), which starts the app in its default mode and also requires:
     * `FLASK_SECRET_KEY`: The secret key for CORS protection; and
     * `PORT`: The port for the host (**note**: this is provided by CF);
     * `POSTGRES_SERVICE`: The name of the PostgreSQL service, as it 
     appears in `VCAP_SERVICES`; and
     * `VCAP_SERVICES`: The credentials for the services the app can
     interact with (**note**: this is provided by CF).

Whenever `py.test` is run with the `--runslow` option (which is used by
default for `python setup.py test`) the `FLASK_CONFIG` must be set to 
`test`.

In addition, for automatic deployment from Travis to Cloud Foundry, the 
following environment variables are required: `CF_ORG`; `CF_SPACE`; 
`CF_USERNAME`; and `CF_PASSWORD`.

The easiest way to set up a database locally, assuming that you're on OS
X with [Homebrew], is:

    brew install postgresql
    psql -c 'create database flask_test;' -U postgres
    
This creates the required test DB using the default PostgreSQL user.

  [1]: https://travis-ci.org/textbook/flask-forecaster.svg?branch=master
  [2]: https://travis-ci.org/textbook/flask-forecaster
  [3]: https://coveralls.io/repos/github/textbook/flask-forecaster/badge.svg?branch=master
  [4]: https://coveralls.io/github/textbook/flask-forecaster?branch=master
  [5]: https://readthedocs.org/projects/flask-forecaster/badge/?version=latest
  [6]: http://flask-forecaster.readthedocs.org/en/latest/?badge=latest

  [Homebrew]: http://brew.sh/
