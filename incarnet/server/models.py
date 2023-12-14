from flask import current_app
from incarnet.server import db, bcrypt
from sqlalchemy.sql import func

class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))

    scan_date = db.Column(db.DateTime(), server_default=func.now())

    @staticmethod
    def gen_hash(value):
        return bcrypt.generate_password_hash(
            value, current_app.config.get("BCRYPT_LOG_ROUNDS")
        )
    
    def __init__(self, username, password):
        self.password = self.gen_hash(password)
        self.username = username
