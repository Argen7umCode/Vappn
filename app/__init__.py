from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from utils.manager_vpn import ManagerVPN
import os

vpn_server_ip = os.getenv('VPN_SERVER_IP')
vpn_server_user = os.getenv('VPN_SERVER_USER')
vpn_server_password = os.getenv('VPN_SERVER_PASSWORD')


manager = ManagerVPN(vpn_server_ip, 
                     vpn_server_user, 
                     vpn_server_password)
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
