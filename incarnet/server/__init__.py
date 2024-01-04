import chromadb
import llm
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

from incarnet.server.config import apply_config

app = Flask(__name__)

with app.app_context():
    apply_config()

CORS(app)

db = SQLAlchemy(app)

model = llm.get_model(app.config.get("LLM_MODEL"))

with app.app_context():
    db.create_all()
    chroma = chromadb.PersistentClient(path=app.instance_path + "/chroma/")

    model.key = app.config.get("OPENAI_API_KEY", "")

bcrypt = Bcrypt(app)

socketio = SocketIO(app, cors_allowed_origins=["http://localhost:8000"])

jwt =  JWTManager(app)

migrate = Migrate(app, db)

import incarnet.server.commands

from .helloworld.views import hello_blueprint
app.register_blueprint(hello_blueprint)

from .auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from .fs.views import fs_blueprint
app.register_blueprint(fs_blueprint)

from .ai.views import ai_blueprint
app.register_blueprint(ai_blueprint)
