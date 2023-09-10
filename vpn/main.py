from fastapi import FastAPI

app = FastAPI()


@app.post('/users/{user_id}')
def create_user():
    pass

@app.delete('/users/{user_id}')
def delete_user():
    pass

@app.get('/users/{user_id}')
def get_user():
    pass



def create_config():
    pass

def delete_config():
    pass

def get_config():
    pass 


