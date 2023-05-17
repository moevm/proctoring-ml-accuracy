import json
import pprint
import uvicorn
from fastapi import FastAPI, Form
from config import XQ_HOST, XQ_PORT, XQ_USERNAME, XQ_PASSWORD

app = FastAPI()


@app.post('/xqueue/login/')
def xqueue_login(username=Form(), password=Form()):
    if username == XQ_USERNAME and password == XQ_PASSWORD:
        return {'return_code': 0}
    return {'return_code': 1}


@app.get('/xqueue/get_submission/')
def xqueue_get_submission(queue_name: str):
    pprint.pprint(queue_name)
    x_header = {
        'submission_id': '<id>',
        'submission_key': '<key>'
    }
    x_body = {
        'token': 'token',
        'data': {
            'student_data': [
                'http://video.mp4',
            ],
            'student_info': [
                'http://photo.jpeg'
            ]
        }
    }
    x_files = {
        'anything': ''
    }
    data = {
        'xqueue_header': json.dumps(x_header),
        'xqueue_body': json.dumps(x_body),
        'xqueue_files': json.dumps(x_files)
    }
    # ToDo: send to test
    return {'content': json.dumps(data)}


@app.post('/xqueue/put_result/')
def xqueue_put_result(xqueue_header=Form(), xqueue_body=Form()):
    # ToDo: result testing
    # result = json.loads(xqueue_body)['result']
    # message = json.loads(xqueue_body)['msg']
    pprint.pprint(f'xqueue_header:\n{xqueue_header}')
    pprint.pprint(f'xqueue_body:\n{xqueue_body}')
    return {'result_code': 0}


if __name__ == '__main__':
    uvicorn.run('xqueue:app', host=XQ_HOST, port=XQ_PORT)
