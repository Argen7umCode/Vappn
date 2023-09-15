from fastapi import FastAPI
from vpn_manager import VPNmanager


app = FastAPI()
manager = VPNmanager()


@app.post('users/configs/{name}')
async def create_config(name):
    config = manager.make_and_get_config(name)
    return config

@app.delete('users/configs')
async def delete_config():
    pass

@app.get('users/configs')
async def get_config():
    pass 


