from pathlib import Path
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from incarnet.filesystem.utils import get_path, rel_path

fs_blueprint = Blueprint("fs_blueprint", __name__)

class FileListAPI(MethodView):
    @jwt_required()
    def get(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        if not real_path.is_dir:
            return jsonify({"msg": "not a dir"}), 400
        res = list(real_path.glob("*"))
        files = [str(rel_path(i)) for i in res if i.is_file()]
        dirs = [str(rel_path(i)) for i in res if i.is_dir()]
        return jsonify({"files": files, "dirs": dirs})

fs_blueprint.add_url_rule(
    "/fs/ls", view_func=FileListAPI.as_view("file_list_api"), methods=["GET"]
)