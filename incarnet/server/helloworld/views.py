from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

hello_blueprint = Blueprint("hello_blueprint", __name__)

class HelloWorldAPI(MethodView):
    def get(self):
        return jsonify({"hello": "world"})

class AuthedHelloWorldAPI(MethodView):
    @jwt_required()
    def get(self):
        return jsonify({"hello": "world (authed)"})

hello_blueprint.add_url_rule(
    "/test/helloworld", view_func=HelloWorldAPI.as_view("hello_world_api"), methods=["GET"]
)
hello_blueprint.add_url_rule(
    "/test/helloworld-auth", view_func=AuthedHelloWorldAPI.as_view("authed_hello_world_api"), methods=["GET"]
)
