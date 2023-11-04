from os import getenv, path
from flask import current_app
import yaml

sqlalchemy_base = "sqlite:///incarnet"


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = sqlalchemy_base + ".db"
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = sqlalchemy_base + "_dev" + ".db"
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    pass


def overlay_config(base, config_file=None):
    """Reading from a YAML file, this overrides configuration options from the bases above."""
    config_locations = [config_file, "/etc/incarnet/config.yml", "./config.yml"]

    config_path = ""

    for loc in config_locations:
        if not loc:
            continue
        if path.exists(loc):
            config_path = loc
            break

    if config_path == "":
        raise FileNotFoundError(
            "Please create a configuration: copy config.yml.example to config.yml."
        )

    config = yaml.safe_load(open(config_path))

    if config["JWT_SECRET_KEY"] == "" or config["JWT_SECRET_KEY"] is None:
        raise ValueError("Please set JWT_SECRET_KEY within the configuration.")

    current_app.config.from_object(base)

    for k, v in config.items():
        current_app.config[k] = v

def apply_config():
    with current_app.app_context():
        if current_app.config["DEBUG"]:
            overlay_config(DevelopmentConfig)
            current_app.logger.warning(
                "Running in DEVELOPMENT MODE; do NOT use this in production!"
            )
        else:
            overlay_config(ProductionConfig)

