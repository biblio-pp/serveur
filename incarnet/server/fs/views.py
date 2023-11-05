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


class FileReadAPI(MethodView):
    @jwt_required()
    def get(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        if not real_path.is_file():
            return jsonify({"msg": "not a file"}), 400
        with open(real_path, mode="r") as f:
            data = f.read()
        return jsonify({"content": data})

fs_blueprint.add_url_rule(
    "/fs/read", view_func=FileReadAPI.as_view("file_read_api"), methods=["GET"]
)


class FileDelAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        if not real_path.is_file():
            return jsonify({"msg": "not a file"}), 400
        real_path.unlink()
        return jsonify({"msg": "deleted"})

fs_blueprint.add_url_rule(
    "/fs/del", view_func=FileDelAPI.as_view("file_delete_api"), methods=["POST"]
)


class FileWriteAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        txt = request.get_json().get("content", "")
        real_path = get_path(path)
        if real_path.is_dir():
            return jsonify({"msg": "is a dir"}), 400
        with open(real_path, mode="w") as f:
            f.write(txt)
        return jsonify({"msg": "written"})

fs_blueprint.add_url_rule(
    "/fs/write", view_func=FileWriteAPI.as_view("file_write_api"), methods=["POST"]
)


class FileMoveAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        new_path = request.args.get("newpath", "")
        real_path = get_path(path)
        real_new_path = get_path(new_path)
        if real_new_path.exists():
            return jsonify({"msg": "already exists"}), 400
        real_path.rename(real_new_path)
        return jsonify({"msg": "moved"})

fs_blueprint.add_url_rule(
    "/fs/mv", view_func=FileMoveAPI.as_view("file_move_api"), methods=["POST"]
)
