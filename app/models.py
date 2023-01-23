from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    telegram_id = db.Column(db.String(250), unique=True)   
