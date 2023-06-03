import os
import json
import glob


class AnswerPull:
    def __init__(self, save_path: str):
        self.save_path = save_path
        self.results = []
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        # Todo: Load result
        if self.index < len(self.results):
            content = self.results[self.index]
            self.index += 1
            return content
        raise StopIteration

    def save_answer(self, index: int, answer):
        # Todo: Save result
        self.results.append([index, answer])


# -------------------------------------------------------------------------------

class TestPull:
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

    def data_gen(self, index, test_file):
        test_id = int(self.directs[index].rsplit('/', 1)[-1])

        body = {
            'token': str(self.index),
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
            'xqueue_header': json.dumps({'submission_id': str(test_id), 'submission_key': str(test_id)}),
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
    test = TestPull('tests')
    for i in test.get_iterator('window.mp4'):
        print(i)
    for i in test.get_iterator('webcam.mp4'):
        print(i)
