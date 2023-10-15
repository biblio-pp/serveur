from flask import Blueprint, jsonify
from flask.views import MethodView

hello_blueprint = Blueprint("hello_blueprint", __name__)

class HelloWorldAPI(MethodView):
    def get(self):
        return jsonify({"hello": "world"})

hello_blueprint.add_url_rule(
    "/test/helloworld", view_func=HelloWorldAPI.as_view("hello_world_api"), methods=["GET"]
)
