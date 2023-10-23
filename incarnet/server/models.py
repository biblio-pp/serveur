from flask import current_app
from incarnet.server import db, bcrypt

class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))

    @staticmethod
    def gen_hash(value):
        return bcrypt.generate_password_hash(
            value, current_app.config.get("BCRYPT_LOG_ROUNDS")
        )
    
    def __init__(self, username, password):
        self.password = self.gen_hash(password)
        self.username = username
