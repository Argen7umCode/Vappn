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
    # TODO сделать проверку в базе данных, если конфиг и таким именем уже есть 
    # то выдать Already exists

    """
        user_id - id пользователя, который является владельцем конфигурации
        client_name - название для файла конфигурации
    """
    params = request.json
    manager.create_connection()
    client_name = params.get('client_name')
    user_name_line = User.query.filter(User.unique_user_id == params.get('unique_user_id')).first()

    # Делается запрос в базу данных, если пользователь существует, то выполняется тело условия
    if user_name_line is not None:
        user_name = user_name_line.username
        
        # Делается запрос на сервер с VPN создается конфига
        response = manager.register_new_client_and_get_config(client_name)
        
        # Если клиент есть, то выполняется запрос на сохраниение конфига в базе данных,
        # иначе возвращается ошибка 
        if response is not None and response != {}:
            db.session.add(VPN_config(user_id=user_name,
                                     client_name=client_name, 
                                     config=response))
            db.session.commit()
        else: 
            response = 'Username error'
    else: 
        response = 'User not found'
    
    manager.close()
    return {
        'client_name' : client_name, 
        'config' : response
    }


@app.route('/vappn/delete_client_config', methods=['DELETE'])
def delete_config():
    """
        client_name - название для файла конфигурации
    """
    params = request.json
    manager.create_connection()
    client_name = params.get('client_name')

    client_name_line = VPN_config.query.filter(VPN_config.client_name == client_name)
    was_removed = manager.remove_client(client_name)
    if client_name_line.first() is not None and was_removed:
        # print(client_name_line.all())
        client_name_line.delete()
        db.session.commit()
        response = 'Success removed'  
    else:
        response = 'Client not found'

    manager.close()

    return {
        'client_name' : client_name, 
        'config' : response
    }