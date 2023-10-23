from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from incarnet.server.config import apply_config

app = Flask(__name__)

with app.app_context():
    apply_config()

CORS(app)

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

import incarnet.server.commands

from .helloworld.views import hello_blueprint
app.register_blueprint(hello_blueprint)
