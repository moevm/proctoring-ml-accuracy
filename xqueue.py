import os
import json
import pprint
import uvicorn
import argparse
import threading
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from config import XQ_HOST, XQ_PORT, XQ_USERNAME, XQ_PASSWORD, TEST_PATH, WINDOW_QUEUE, WEBCAM_QUEUE, FILE_NAME_QUEUE
from analyzator.pools import TestPool, AnswerPool


app = FastAPI()
tests = TestPool(TEST_PATH)
results = AnswerPool()
test_iters = {
    WINDOW_QUEUE: tests.get_iterator(FILE_NAME_QUEUE[WINDOW_QUEUE]),
    WEBCAM_QUEUE: tests.get_iterator(FILE_NAME_QUEUE[WEBCAM_QUEUE])
}


@app.post('/xqueue/login/')
async def xqueue_login(username=Form(), password=Form()):
    if username == XQ_USERNAME and password == XQ_PASSWORD:
        return {'return_code': 0}
    return {'return_code': 1}


@app.get('/xqueue/get_submission/')
async def xqueue_get_submission(queue_name: str):
    try:
        if test_iters.get(queue_name):
            data = next(test_iters[queue_name])
            return {'content': data}
        return HTMLResponse(status_code=405)
    except StopIteration:
        test_iters.pop(queue_name)
    return HTMLResponse(status_code=405)


@app.post('/xqueue/put_result/')
async def xqueue_put_result(xqueue_header=Form(), xqueue_body=Form()):
    try:
        test_id = int(json.loads(xqueue_header)['submission_id'])
        test_file = json.loads(xqueue_header)['submission_key']
        results.push_answer(test_id, test_file, xqueue_body)
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


def run(args: dict):
    if args['web']:
        tests.set_data_output('web', XQ_HOST + ':' + str(XQ_PORT))
    if args['only_screen']:
        test_iters.pop(WEBCAM_QUEUE)
    elif args['only_camera']:
        test_iters.pop(WINDOW_QUEUE)
    server = uvicorn.Server(uvicorn.Config('xqueue:app', host=XQ_HOST, port=XQ_PORT))
    threading.Thread(target=lambda: server.run(), args=()).start()
    return server


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", action='store_true', help="tests data will contain http address instead of absolute path")
    ap.add_argument("--only_camera", action='store_true', help="only web-camera proctoring testing")
    ap.add_argument("--only_screen", action='store_true', help="only screencast proctoring testing")
    run(vars(ap.parse_args()))
