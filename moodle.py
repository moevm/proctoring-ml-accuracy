import pprint
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from config import ML_HOST, ML_PORT


class Client(BaseModel):
    client_id: str
    client_secret: str


class Logs(BaseModel):
    token: str
    timestamp: float
    event_type: str
    data: str
    attempt: int


token = 'secret-token'
app = FastAPI()


@app.get('/ml/auth/token')
async def ml_auth_token():
    return {
        'client_id': '12345',
        'client_secret': '111',
    }


@app.post('/ml/auth/token')
async def ml_auth_token(client: Client):
    if client.client_id == '12345' and client.client_secret == '111':
        return {'token': token}
    return {'error': 'wrong creds'}


@app.post('/logs')
async def logs(logs: Logs):
    pprint.pprint(logs)
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run('moodle:app', host=ML_HOST, port=ML_PORT)
