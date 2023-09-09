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


url = r'http://127.0.0.1:5000/vappn/create_client_config'


manager = ManagerVPN(VPN_SERVER_IP, VPN_SERVER_USER, VPN_SERVER_PASSWORD)

# TESTS
def test_succses_regiser_config():
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(10),
                "unique_user_id" : randint(5)
            }
        res = requests.post('http://127.0.0.1:5000/vappn/register_user', json=user)

        for i in range(2):
            body = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }

            res = requests.post(url, json=body)
            manager.remove_client(body['client_name'])

            assert re.search(r'[Interface]', res.json()['config']) 

    manager.close()


def test_client_already_exists():
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(2),
                "unique_user_id" : randint(5)
            }
        res = requests.post('http://127.0.0.1:5000/vappn/register_user', json=user)

        for i in range(2):
            body = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }

            res = requests.post(url, json=body)
            res = requests.post(url, json=body)
            manager.remove_client(body['client_name'])

            assert res.json()['config'] == 'Client name already exists'

    manager.close()


def test_user_not_found():
    manager.create_connection()

    with app.app_context():
        user = {
                "username" : get_random_str(2),
                "unique_user_id" : randint(5)
            }

        for i in range(2):
            body = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(10)
            }

            res = requests.post(url, json=body)
            manager.remove_client(body['client_name'])

            assert res.json()['config'] == 'User not found'

    manager.close()