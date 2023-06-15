import os
import json
import pprint
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseSettings
from collector.config import XQ_USERNAME, XQ_PASSWORD, FILE_NAME_QUEUE
from collector.utilities import TestPool, AnswerPool


class Settings(BaseSettings):
    tests: TestPool = None
    results: AnswerPool = AnswerPool()
    test_iters: dict = {}
    queues: list = []


app = FastAPI()
settings = Settings()


# ROUTES

@app.post('/xqueue/login/')
async def xqueue_login(username=Form(), password=Form()):
    if username == XQ_USERNAME and password == XQ_PASSWORD:
        return {'return_code': 0}
    return {'return_code': 1}


@app.get('/xqueue/get_submission/')
async def xqueue_get_submission(queue_name: str):
    try:
        if settings.test_iters.get(queue_name):
            data = next(settings.test_iters[queue_name])
            return {'content': data}
        return HTMLResponse(status_code=405)
    except StopIteration:
        settings.test_iters.pop(queue_name)
    return HTMLResponse(status_code=405)


@app.post('/xqueue/put_result/')
async def xqueue_put_result(xqueue_header=Form(), xqueue_body=Form()):
    try:
        test_id = int(json.loads(xqueue_header)['submission_id'])
        test_file = json.loads(xqueue_header)['submission_key']
        settings.results.push_answer(test_id, test_file, xqueue_body)
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


# API

def refresh():
    settings.results.clear()
    settings.test_iters.clear()
    for i in settings.queues:
        settings.test_iters.update({i: settings.tests.get_iterator(FILE_NAME_QUEUE[i])})


def setup(queues: list, test_pool: TestPool):
    settings.tests = test_pool
    settings.queues = queues
    refresh()


def result():
    return settings.results if len(settings.test_iters) == 0 else None
