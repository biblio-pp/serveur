from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from incarnet.server.config import apply_config

app = Flask(__name__)

with app.app_context():
    apply_config()

CORS(app)

db = SQLAlchemy(app)

from .helloworld.views import hello_blueprint
app.register_blueprint(hello_blueprint)
