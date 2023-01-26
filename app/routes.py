from app import app, db, manager
from app.models import User, VPN_config
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.route('/vappn/register', methods=['POST'])
def register():
    """
        username - username пользователя, который является владельцем конфигурации
        unique_user_id - его уникальный идентификатор   
    """
    params = request.json
    user = User(**params)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'Response' : 'User already exists'})
    else:
        return jsonify({'Response' : 'Succsess'})


@app.route('/vappn/create_client_config', methods=['POST'])
def register_config():
    """
        user_id - id пользователя, который является владельцем конфигурации
        client_name - название для файла конфигурации
    """
    params = request.json
    manager.create_connection()
    client_name = params.get('client_name')
    response = manager.register_new_client_and_get_config(client_name)
    print(client_name)

    if response is not None and response != {}:
        # VPN_config = VPN_config()
        try:
            user_name = User.query.filter(User.unique_user_id == params.get('unique_user_id')).first().username
        except AttributeError:
            response = 'user_name error'
        else: 
            db.session.add(VPN_config(user_id=user_name, config=response))
            db.session.commit()

    manager.close()
    return {
        'client_name' : client_name, 
        'config' : response
    }
