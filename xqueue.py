import os
import json
import pprint
import uvicorn
import argparse
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from config import XQ_HOST, XQ_PORT, XQ_USERNAME, XQ_PASSWORD, TEST_PATH
from analyzator.test_pull import TestPull
from analyzator.analizer import store_res


app = FastAPI()
tests = TestPull(TEST_PATH)
test_iters = {
    'webcam_queue': tests.get_iterator('webcam.mp4'),
    'screencast_queue': tests.get_iterator('window.mp4')
}


@app.post('/xqueue/login/')
async def xqueue_login(username=Form(), password=Form()):
    if username == XQ_USERNAME and password == XQ_PASSWORD:
        return {'return_code': 0}
    return {'return_code': 1}


@app.get('/xqueue/get_submission/')
async def xqueue_get_submission(queue_name: str):
    try:
        data = next(test_iters[queue_name])
        return {'content': data}
    except StopIteration:
        pass
    return HTMLResponse(status_code=405)


@app.post('/xqueue/put_result/')
async def xqueue_put_result(xqueue_header=Form(), xqueue_body=Form()):
    try:
        test_id = int(json.loads(xqueue_header)['submission_id'])
        store_res(test_id, xqueue_body)
    except ValueError | KeyError:
        pprint.pprint('Can not save result from proctoring-ml')
        pprint.pprint(f'xqueue_header:\n{xqueue_header}')
        pprint.pprint(f'xqueue_body:\n{xqueue_body}')
    return {'result_code': 0}


@app.get('/tests/{test_id}/{file_name}')
async def test_data_send(test_id: int, file_name: str):
    if os.path.exists(f'tests/{test_id}/data/{file_name}'):
        return FileResponse(f'tests/{test_id}/data/{file_name}', media_type='application/octet-stream')
    return HTMLResponse(status_code=404)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", action='store_true', help="tests data will contain http address instead of absolute path")
    if vars(ap.parse_args())['web']:
        tests.set_data_output('web', XQ_HOST + ':' + str(XQ_PORT))
    uvicorn.run('xqueue:app', host=XQ_HOST, port=XQ_PORT)
