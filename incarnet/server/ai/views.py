from datetime import datetime
from datetime import timezone
import os
from pathlib import Path
from chromadb import Collection
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from incarnet.filesystem.utils import get_root, rel_path
from incarnet.server.ai.utils import get_user_collection, query_db
from incarnet.server.models import User, db
from incarnet.server import chroma, sock, model
import hashlib

ai_blueprint = Blueprint("ai_blueprint", __name__)

class ScanAPI(MethodView):
    @jwt_required()
    def post(self):
        user: User | None = User.query.filter_by(username=get_jwt_identity()).first()
        if not user:
            return jsonify({
                "msg": "no such user",
            }), 400

        scan_date : datetime = user.scan_date

        user_collection = get_user_collection()

        docs_scanned: list[Path] = []

        root_path = get_root()
        for i in sorted(root_path.glob('**/*'), key=os.path.getmtime, reverse=True):
            if i.is_file():
                if os.path.getmtime(i) < scan_date.timestamp():
                    break
                with i.open('r') as f:
                    content: str = f.read()
                    hsh = hashlib.sha256()
                    hsh.update(content.encode())
                    user_collection.add(documents=[content], ids=[hsh.hexdigest()], metadatas={"path": str(rel_path(i))})
                docs_scanned.append(i)

        user.scan_date = datetime.now()

        db.session.commit()

        return jsonify({
            "msg": "ok",
            "scanned": [str(rel_path(i)) for i in docs_scanned]
        })

ai_blueprint.add_url_rule(
    "/ai/scan", view_func=ScanAPI.as_view("scan_api"), methods=["POST"]
)

@sock.route("/ai/convo")
@jwt_required()
def convo(ws):
    c = model.conversation()

    first_resp: bool = True

    while True:
        data: str = ws.receive()
        if first_resp:
            docs = query_db(data)
            sys_prompt = f"Tu es un tuteur. Aide l'élève à comprendre la matière. Sois concis. Ci-joint sont des documents qui pourraient t'aider:\n" \
                + "\n\n---\n\n".join(docs["documents"][0])
            resp = c.prompt(data, system=sys_prompt)
            ws.send(resp.text())
            first_resp = False
        else:
            resp = c.prompt(data)
            ws.send(resp.text())
