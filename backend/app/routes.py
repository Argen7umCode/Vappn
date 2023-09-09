from app import app, db, manager
from app.models import User, VPN_config
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from pprint import pprint as print
from utils.json_to_get_client_confs import create_json_response_user_id_client_config


def get_query_in_table_by_line_and_value(table, line, value):
    return table.query.filter(line == value)


def get_user_info_dy_userline(userline):
    return {
        'username' : userline.username,
        'unique_user_id' : userline.unique_user_id
    }


@app.route('/vappn/register_user', methods=['POST'])
def register_user():
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


@app.route('/vappn/get_user', methods=['GET'])
def get_user():
    params = request.json
    user_id = params.get('user_id')
    if user_id is None:
        userinfo = [get_user_info_dy_userline(userline) for userline in User.query.all()]
        if userinfo == []:
            userinfo = 'Users table is'
    else:
        userline = get_query_in_table_by_line_and_value(User, User.unique_user_id, user_id).one()
        userinfo = get_user_info_dy_userline(userline)
    return userinfo


@app.route('/vappn/delete_user', methods=['DELETE'])
def delete_user_by_unique_id():
    params = request.json
    user_id = params.get('user_id')

    user_name_line = get_query_in_table_by_line_and_value(User,
                                                        User.unique_user_id, 
                                                        user_id)

    if user_name_line.all() != []:
        client_configs_by_user_id = get_query_in_table_by_line_and_value(VPN_config,
                                                    VPN_config.user_id,
                                                    user_id).all()

        print(client_configs_by_user_id)
        if client_configs_by_user_id != []:
            manager.create_connection()

            deleting_result = {}
            for line in client_configs_by_user_id:
                client_config = line.client_name 
                deleting_result[client_config] = manager.remove_client(client_config) 

                db.session.delete(line)
                db.session.commit()
        else:
            deleting_result = 'Empty user'

        db.session.delete(user_name_line.one())
        db.session.commit()

        response = deleting_result
    else:
        response = 'User not found'
    
    return {
            'user_id' : user_id, 
            'response': response
    }


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
    unique_user_id = params.get('unique_user_id')

    user_line = get_query_in_table_by_line_and_value(
                                                    User, 
                                                    User.unique_user_id, 
                                                    unique_user_id
                                                ).first()

    # Делается запрос в базу данных, если пользователь существует, то выполняется тело условия
    if get_query_in_table_by_line_and_value(VPN_config,
                                            VPN_config.client_name, 
                                            client_name).all() == []:
        if user_line is not None:
            # Делается запрос на сервер с VPN создается конфига
            response = manager.register_new_client_and_get_config(client_name)
            # Если клиент есть, то выполняется запрос на сохраниение конфига в базе данных,
            # иначе возвращается ошибка 
            if response is not None and response != '':
                db.session.add(VPN_config(user_id=unique_user_id,
                                        client_name=client_name, 
                                        config=response))
                db.session.commit()
            else: 
                response = 'Username error'
        else: 
            response = 'User not found'
    else:
        response = 'Client name already exists'
        
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

    client_name_line = get_query_in_table_by_line_and_value(VPN_config, 
                                                            VPN_config.client_name, 
                                                            client_name)
    was_removed = manager.remove_client(client_name)
    if client_name_line.first() is not None and was_removed:
        client_name_line.delete()
        db.session.commit()
        response = 'Success removed'  
    else:
        response = 'Client not found'

    manager.close()

    return {
        'client_name' : client_name, 
        'response' : response
    }


@app.route('/vappn/get_client_configs', methods=['GET'])
def get_config():
    '''
        user_id - уникальный идентификационный номер пользователя 
    '''
    params = request.json
    user_id = params.get('user_id')

    user_name_line = get_query_in_table_by_line_and_value(User,
                                                          User.unique_user_id, 
                                                          user_id).all()

    if user_name_line != []:
        data = get_query_in_table_by_line_and_value(VPN_config,
                                                    VPN_config.user_id,
                                                    user_id).all()
        response = create_json_response_user_id_client_config(user_id, data)
    else:
        response = {
            user_id : 'User not found'
        }

    return response


