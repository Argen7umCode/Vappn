import pytest
import requests
import random
import os 



import sys
sys.path[0] = '/'.join(sys.path[0].split('/')[:-1])

from app import db, app
from app.models import User


url = r'http://127.0.0.1:5000/vappn/register'

def get_random_str(length):
    return ''.join(str(random.randint(0, 9)) for i in range(length))

# TESTS
def test_succses_regiser():
    with app.app_context():
        for i in range(100):
            body = {
                "username" : get_random_str(10),
                "unique_user_id" : get_random_str(10)
            }

            res = requests.post(url, json=body)
            User.query.filter(User.unique_user_id == body['unique_user_id']).delete()
            db.session.commit()

            assert res.json()['Response'] == 'Succsess'

def test_already_exists():
    with app.app_context():
        for i in range(100):
            body = {
                "username" : get_random_str(10),
                "unique_user_id" : get_random_str(10)
            }

            res = requests.post(url, json=body)
            res = requests.post(url, json=body)
            User.query.filter(User.unique_user_id == body['unique_user_id']).delete()
            db.session.commit()

            assert res.json()['Response'] == 'User already exists'
# print(get_random_str(10))