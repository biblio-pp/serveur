from pathlib import Path
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from incarnet.filesystem.utils import get_path, get_root, rel_path

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
        data = real_path.read_text()
        return jsonify({"content": data})

fs_blueprint.add_url_rule(
    "/fs/read", view_func=FileReadAPI.as_view("file_read_api"), methods=["GET"]
)


class FileDelAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        try:
            if real_path.is_file():
                real_path.unlink()
            elif real_path.is_dir():
                real_path.rmdir()
        except FileNotFoundError:
            return jsonify({"msg": "does not exist"}), 400
        except OSError:
            return jsonify({"msg": "dir not empty"}), 400
        else:
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
        real_path.write_text(txt)
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

class DirCreateAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        if real_path.exists():
            return jsonify({"msg": "already exists"}), 400
        real_path.mkdir()
        return jsonify({"msg": "created"})

fs_blueprint.add_url_rule(
    "/fs/mkdir", view_func=DirCreateAPI.as_view("dir_create_api"), methods=["POST"]
)

class TouchAPI(MethodView):
    @jwt_required()
    def post(self):
        path = request.args.get("path", "")
        real_path = get_path(path)
        if real_path.is_dir():
            return jsonify({"msg": "is dir"}), 400
        real_path.touch()
        return jsonify({"msg": "touched"})

fs_blueprint.add_url_rule(
    "/fs/touch", view_func=TouchAPI.as_view("touch_api"), methods=["POST"]
)

class SearchAPI(MethodView):
    @jwt_required()
    def get(self):
        query = request.args.get("query", None)
        if not query:
            return jsonify({"msg": "no query"}), 400

        files = []

        root_path = get_root()
        for i in root_path.glob('**/*'):
            if i.is_file():
                with i.open('r') as f:
                    if query.lower() in f.read().lower():
                        files.append(i)
                        continue
            if query.lower() in str(i).lower():
                files.append(i)

        return jsonify({"msg": "success", "data": [str(rel_path(i)) for i in files]})

fs_blueprint.add_url_rule(
    "/fs/search", view_func=SearchAPI.as_view("search_api"), methods=["GET"]
)
