from incarnet.server import db

class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
