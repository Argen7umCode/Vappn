import pytest
import requests
from get_random_str import get_random_str, randint
import sys
from dotenv import load_dotenv
import os 
import re
load_dotenv()
VPN_SERVER_IP = os.getenv('VPN_SERVER_IP')
VPN_SERVER_USER = os.getenv('VPN_SERVER_USER')
VPN_SERVER_PASSWORD = os.getenv('VPN_SERVER_PASSWORD')


sys.path[0] = '/'.join(sys.path[0].split('/')[:-1])

from utils.manager_vpn import ManagerVPN
from app import db, app
from app.models import User, VPN_config


url = 'http://127.0.0.1:5000/vappn/delete_client_config'


manager = ManagerVPN(VPN_SERVER_IP, VPN_SERVER_USER, VPN_SERVER_PASSWORD)

# TESTS
def test_succsess_deleting_config():
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(10),
                "unique_user_id" : randint(5)
            }
        res = requests.post('http://127.0.0.1:5000/vappn/register_user', json=user)

        for i in range(2):
            config = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }

            res = requests.post(r'http://127.0.0.1:5000/vappn/create_client_config', json=config)
            del_json = {
                "client_name" : config['client_name']
            }
            res = requests.delete(url, json=del_json)

            assert res.json()['response'] == 'Success removed'  

    manager.close()


def test_client_not_found_deleting_config():
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(10),
                "unique_user_id" : randint(5)
            }
        res = requests.post('http://127.0.0.1:5000/vappn/register_user', json=user)

        for i in range(2):
            config = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }
            res = requests.post(r'http://127.0.0.1:5000/vappn/create_client_config', json=config)
            manager.remove_client(config['client_name'])
            
            del_json = {
                "client_name" : config['client_name']
            }
            res = requests.delete(url, json=del_json)

            assert res.json()['response'] == 'Client not found'  

    manager.close()


