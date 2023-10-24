from flask import Blueprint, request, jsonify
from flask.views import MethodView
from incarnet.server import bcrypt
from incarnet.server.models import User
from flask_jwt_extended import create_access_token, unset_jwt_cookies

auth_blueprint = Blueprint("auth_blueprint", __name__)

class LoginAPI(MethodView):
    def post(self):
        username = request.get_json().get("username", None)
        password = request.get_json().get("password", None)

        if username == None or password == None:
            return jsonify({"msg": "Need `username` and `password` field."}), 401

        user = User.query.filter_by(username=username).first()
        if user == None:
            return jsonify({"msg": "Invalid credentials."}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials."}), 401

        tok = create_access_token(identity=username)
        return jsonify({"token": tok, "username": username})

auth_blueprint.add_url_rule("/auth/login", view_func=LoginAPI.as_view("login_api"), methods=["POST"])


class LogoutAPI(MethodView):
    def post(self):
        resp = jsonify({"msg": "logged out"})
        unset_jwt_cookies(resp)
        return resp

auth_blueprint.add_url_rule("/auth/logout", view_func=LogoutAPI.as_view("logout_api"), methods=["POST"])
