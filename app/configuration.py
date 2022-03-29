from os import environ


class BaseConfig:
    DEBUG = False
    TESTING = False
    DATABASE_URL = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")
    TOKEN_EXPIRES = environ.get("TOKEN_EXPIRES", 120)


class ProductionConfig(BaseConfig):
    ENV = "production"
    LOG_LEVEL = "INFO"


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class TestingConfig(BaseConfig):
    ENV = "test"
    TESTING = True
    LOG_LEVEL = "DEBUG"
    SECRET_KEY = environ.get("SECRET_KEY", "test-secret-key")
    DATABASE_URL = environ.get("DATABASE_URL", "test_sqlite")


config_by_name = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig,
)
