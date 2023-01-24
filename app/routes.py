from app import app, db
from app.models import User
from flask import request, jsonify


@app.route('/vappn/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    db.session.add(user)
    db.session.commit()

    return f'<h1>{params}</h1>'


@app.route('/vappn/get_config', methods=['GET'])
def get_config():
    params = request.json