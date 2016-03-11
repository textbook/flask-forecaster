import io
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--pylint',
            '--pylint-error-types=FEW',
            '--runslow',
            '--driver=Firefox',
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    author='Jonathan Sharpe',
    author_email='jsharpe@pivotal.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass={'test': PyTest},
    description=('A Flask-based web app for forecasting Pivotal Tracker '
                 'projects.'),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'psycopg2',
        'requests',
    ],
    license='License :: OSI Approved :: ISC License (ISCL)',
    long_description=long_description,
    name='flask_forecaster',
    package_data={
        'static': 'flask_forecaster/static/*',
        'templates': 'flask_forecaster/templates/*',
    },
    packages=['flask_forecaster'],
    platforms='any',
    tests_require=[
        'pytest',
        'pytest-flask',
        'pytest-pylint',
        'pytest-selenium',
        'responses',
    ],
    url='http://github.com/textbook/flask-forecaster/',
    version='0.0.5',
)