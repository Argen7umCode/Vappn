from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    unique_user_id = db.Column(db.String(250), unique=True)   
    configs = db.relationship('VPN_config', backref='user')

    # def __init__(self, **kwargs) -> None:
    #     self.username = kwargs.get('username')
    #     self.telegram_id = kwargs.get('telegram_id')
        
    def __repl__(self):
        return f'{self.username} {self.unique_user_id   }'


class VPN_config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    config = db.Column(db.Text)

    # def __init__(self, **kwargs) -> None:
    #     self.user_id = kwargs.get('user_id', db.ForeignKey('user.id'))
    #     self.config = kwargs.get('config')
        