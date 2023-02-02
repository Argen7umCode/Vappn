import pytest
import requests
from get_random_str import get_random_str, randint
import sys
from dotenv import load_dotenv
import os 
load_dotenv()
VPN_SERVER_IP = os.getenv('VPN_SERVER_IP')
VPN_SERVER_USER = os.getenv('VPN_SERVER_USER')
VPN_SERVER_PASSWORD = os.getenv('VPN_SERVER_PASSWORD')


sys.path[0] = '/'.join(sys.path[0].split('/')[:-1])

from utils.manager_vpn import ManagerVPN
from app import db, app
from app.models import User, VPN_config


url = r'http://127.0.0.1:5000/vappn/create_client_config'


manager = ManagerVPN(VPN_SERVER_IP, VPN_SERVER_USER, VPN_SERVER_PASSWORD)

# TESTS
def test_succses_regiser_config():
    print(manager.ip)
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(10),
                "unique_user_id" : randint(5)
            }
        print(user)
        print(requests.post('http://127.0.0.1:5000/vappn/register', json=user).json())
        
        
        for i in range(1):
            body = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }
            print(body)

            res = requests.post(url, json=user)
            print(res.json())
            manager.remove_client(body['client_name'])

            assert res.json()['config'] != 'user_name error'

            
            # User.query.filter(VPN_config.user_id == body['unique_user_id']).delete()
            
            db.session.commit()
    manager.close()
        # User.query.filter(User.unique_user_id == body['unique_user_id']).delete()
        # db.session.commit()

# def test_already_exists():
#     with app.app_context():
#         for i in range(100):
#             body = {
#                 "username" : get_random_str(10),
#                 "unique_user_id" : get_random_str(10)
#             }

#             res = requests.post(url, json=body)
#             res = requests.post(url, json=body)
#             User.query.filter(User.unique_user_id == body['unique_user_id']).delete()
#             db.session.commit()

#             assert res.json()['Response'] == 'User already exists'
