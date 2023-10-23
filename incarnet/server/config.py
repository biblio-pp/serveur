from flask import current_app


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///incarnet.db"
    SECRET_KEY = "asdfasdfasdfasdf"
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATION = False


def apply_config():
    current_app.config.from_object(Config)
