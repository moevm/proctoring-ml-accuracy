import os
import json
import pprint
import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from config import XQ_HOST, XQ_PORT, XQ_USERNAME, XQ_PASSWORD
from test import Tests

app = FastAPI()
tests = Tests('tests', XQ_HOST + ':' + str(XQ_PORT))


@app.post('/xqueue/login/')
def xqueue_login(username=Form(), password=Form()):
    if username == XQ_USERNAME and password == XQ_PASSWORD:
        return {'return_code': 0}
    return {'return_code': 1}


@app.get('/xqueue/get_submission/')
def xqueue_get_submission(queue_name: str):
    pprint.pprint(queue_name)
    # ToDo: send to test
    data = tests.curr()
    if data is not None:
        tests.next()
        return {'content': json.dumps(data)}
    return {'content': {}}


@app.post('/xqueue/put_result/')
def xqueue_put_result(xqueue_header=Form(), xqueue_body=Form()):
    # ToDo: result testing
    # result = json.loads(xqueue_body)['result']
    # message = json.loads(xqueue_body)['msg']
    pprint.pprint(f'xqueue_header:\n{xqueue_header}')
    pprint.pprint(f'xqueue_body:\n{xqueue_body}')
    return {'result_code': 0}


@app.get('/tests/{test_id}/data/{file_name}')
def test_data_send(test_id: int, file_name: str):
    pprint.pprint(f'{test_id}, {file_name}')
    if os.path.exists(f'tests/{test_id}/data/{file_name}'):
        return FileResponse(f'tests/{test_id}/data/{file_name}', media_type='application/octet-stream')
    return HTMLResponse(status_code=404)


if __name__ == '__main__':
    uvicorn.run('xqueue:app', host=XQ_HOST, port=XQ_PORT)
