from flask import Blueprint
from flask.views import MethodView
from incarnet.server import db

auth_blueprint = Blueprint("auth_blueprint", __name__)

class LoginAPI(MethodView):
    pass
