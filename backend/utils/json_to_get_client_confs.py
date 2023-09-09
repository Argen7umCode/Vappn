def create_json_response_user_id_client_config(user_id, data):
    return {
        user_id : [{
            'client_name' : line.client_name,
            'config' : line.config
        } for line in data] 
    }
