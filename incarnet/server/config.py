from datetime import timedelta
from flask import current_app


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///incarnet.db"
    JWT_SECRET_KEY = "asdfasdfasdfasdf"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATION = False


def apply_config():
    current_app.config.from_object(Config)
