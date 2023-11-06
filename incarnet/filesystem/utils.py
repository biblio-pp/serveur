from pathlib import Path
from flask_jwt_extended import get_jwt_identity
from flask import current_app


def san_path(p: Path):
    root_path = Path(current_app.config["INCARNET_FILE_DIR"])
    if not root_path.is_absolute():
        root_path = Path(current_app.instance_path) / root_path
    real_root = root_path.resolve()
    desired = (real_root / p).resolve()
    if desired in real_root.parents:
        raise ValueError("Path outside of root")
    return desired

def get_root():
    username: str = get_jwt_identity()
    path: Path = san_path(Path(username))
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_path(p: str):
    path = Path(p)
    if path.is_absolute():
        rp = Path(p).relative_to("/")
    else:
        rp = Path(p)
    return san_path(get_root() / rp)

def rel_path(p: Path):
    return p.relative_to(get_root())
