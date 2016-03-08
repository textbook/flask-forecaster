import io
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

import flask_forecaster

if sys.version_info < (3, 5):
    err_msg = '{} requires Python 3.5 or above'.format(halliwell.__name__)
    raise RuntimeError(err_msg)


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
        self.test_args = ['--pylint', '--runslow', '--driver=Firefox']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    author=flask_forecaster.__author__,
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
    description=flask_forecaster.__doc__,
    install_requires=[],
    license='License :: OSI Approved :: ISC License (ISCL)',
    long_description=long_description,
    name='flask_forecaster',
    packages=['flask_forecaster'],
    platforms='any',
    tests_require=[
        'pytest',
        'pytest-flask',
        'pytest-pylint',
    ],
    url='http://github.com/textbook/flask-forecaster/',
    version=flask_forecaster.__version__,
)