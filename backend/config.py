import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    VPN_SERVER_IP = os.getenv('VPN_SERVER_IP')
    VPN_SERVER_USER = os.getenv('VPN_SERVER_USER')
    VPN_SERVER_PASSWORD = os.getenv('VPN_SERVER_PASSWORD')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database/vappn.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False