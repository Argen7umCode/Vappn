from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    telegram_id = db.Column(db.String(250), unique=True)   

    def __init__(self, **kwargs) -> None:
        self.username = kwargs.get('username')
        self.telegram_id = kwargs.get('telegram_id')
        

    def __repl__(self):
        return f'{self.username} {self.telegram_id}'

