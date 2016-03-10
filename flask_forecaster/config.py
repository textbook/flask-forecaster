"""Flask configuration options."""

import os


class DefaultConfig:
    """Configuration defaults."""

    DEBUG = False
    SECRET_KEY = 'youwillneverguessme'
    TESTING = False


class DevelopmentConfig(DefaultConfig):
    """Configuration for development (local)."""

    DEBUG = True


class TestingConfig(DefaultConfig):
    """Configuration for testing (Travis CI)."""

    TESTING = True


class ProductionConfig(DefaultConfig):
    """Configuration for deployment (Cloud Foundry)."""

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
