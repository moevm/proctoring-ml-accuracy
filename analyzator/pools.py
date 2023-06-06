import os
import json
import glob
from config import WINDOW_QUEUE, WEBCAM_QUEUE, FILE_NAME_QUEUE


class AnswerPool:
    def __init__(self):
        self.results = []

    def get_window_results(self):
        results = []
        for i in self.results:
            if i['queue'] == WINDOW_QUEUE:
                results.append(i)
        return results

    def get_webcam_results(self):
        results = []
        for i in self.results:
            if i['queue'] == WEBCAM_QUEUE:
                results.append(i)
        return results

    def push_answer(self, index: int, queue_type: str, answer: str):
        if queue_type in FILE_NAME_QUEUE.keys():
            answer = json.loads(answer)
            done_answer = {
                "result": {
                    "warn": [],
                    "ok": []
                },
                "elapsed_time": answer['result']['elapsed_time'],
                "msg": answer['msg']
            }
            for i in answer['result']['frame_data']:
                for j in i.keys():
                    if done_answer.get(j):
                        done_answer['result'][j] += i[j]
            self.results.append({'index': index, 'queue': queue_type, 'answer': answer})

    def save_local(self, save_path: str):
        for i in self.results:
            file_name = FILE_NAME_QUEUE[i['queue']].split('.', 1)[0] + '_' + i['index'] + '.json'
            with open(f'{save_path}/{file_name}', 'w') as f:
                f.write(i['answer'])


# -------------------------------------------------------------------------------

class TestPool:
    class Iterator:
        def __init__(self, iterable, test_type: str):
            self.index = 0
            self.iterable = iterable
            self.test_type = test_type

        def __iter__(self):
            self.index = 0
            return self

        def __next__(self):
            if self.index < len(self.iterable.directs):
                self.index += 1
                return self.iterable.data_gen(self.index - 1, self.test_type)
            raise StopIteration

    def __init__(self, test_path: str):
        self.host_port = None
        self.directs = sorted(glob.glob(test_path + '/*'))
        self.index = 0

    def get_iterator(self, test_type):
        return self.Iterator(self, test_type)

    def data_gen(self, index, test_file: str):
        test_id = int(self.directs[index].rsplit('/', 1)[-1])

        body = {
            'token': str(test_id),
            'data': {
                'student_data': [],
                'student_info': []
            }
        }

        if self.host_port is None:
            file_source = os.path.abspath(f'{self.directs[self.index]}/data') + '/'
        else:
            file_source = f'http://{self.host_port}/tests/{test_id}/'

        photos = glob.glob(f'{self.directs[self.index]}/data/photo.*')
        if len(photos) > 0:
            body['data']['student_info'].append(file_source + photos[0].rsplit("/", 1)[-1])
        else:
            print(f'There is no photo in test "{test_id}"')

        if os.path.exists(f'{self.directs[self.index]}/data/{test_file}'):
            body['data']['student_data'].append(file_source + test_file)
        else:
            print(f'There is no video in test "{test_id}"')

        content = {
            'xqueue_header': json.dumps({'submission_id': str(test_id), 'submission_key': test_file.split('.', 1)[0]}),
            'xqueue_body': json.dumps(body),
            'xqueue_files': json.dumps({'anything': ''})
        }
        return json.dumps(content)

    def get_test(self, index: int, test_file):
        return self.data_gen(index, test_file) if 0 <= index < len(self.directs) else None

    def set_data_output(self, o_type: str, address=None):
        if o_type == 'local':
            self.host_port = None
        elif o_type == 'web' and address is not None:
            self.host_port = address


# -------------------------------------------------------------------------------

if __name__ == '__main__':
    pass
