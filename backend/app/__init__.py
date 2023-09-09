from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from utils.manager_vpn import ManagerVPN


app = Flask(__name__)
app.config.from_object(Config)

manager = ManagerVPN(app.config['VPN_SERVER_IP'], 
                     app.config['VPN_SERVER_USER'], 
                     app.config['VPN_SERVER_PASSWORD'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
