import pytest
import requests
import random, string

import sys
sys.path[0] = '/'.join(sys.path[0].split('/')[:-1])

from app import db, app, manager
from app.models import User, VPN_config


url = r'http://127.0.0.1:5000/vappn/create_client_config'

def get_random_str(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# TESTS
def test_succses_regiser_config():
    manager.create_connection()
    with app.app_context():
        user = {
                "username" : get_random_str(10),
                "unique_user_id" : get_random_str(10)
            }
        
        requests.post(url, json=user)
        
        
        for i in range(1):
            body = {
                "unique_user_id" : user['unique_user_id'],
                "client_name" : get_random_str(50)
            }
            print(body)

            res = requests.post(url, json=user)
            
            manager.remove_client(body['client_name'])

            assert res.json()['config'] != 'user_name error'

            
            # User.query.filter(VPN_config.user_id == body['unique_user_id']).delete()
            
            # db.session.commit()
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
test_succses_regiser_config()