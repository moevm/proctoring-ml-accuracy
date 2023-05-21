import os
import json
import glob
import pprint


class Tests:
    def __init__(self, test_path: str, host_port: str | None = None):
        self.index = 0
        self.host_port = host_port
        self.directs = sorted(glob.glob(test_path + '/*'))

    def data_gen(self, v_file: str):
        test_id = int(self.directs[self.index].rsplit('/', 1)[-1])

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
            pprint.pprint(f'There is no photo in test "{test_id}"')

        if os.path.exists(f'{self.directs[self.index]}/data/{v_file}'):
            body['data']['student_data'].append(file_source + v_file)
        else:
            pprint.pprint(f'There is no video in test "{test_id}"')

        content = {
            'xqueue_header': json.dumps({'submission_id': str(test_id), 'submission_key': str(test_id)}),
            'xqueue_body': json.dumps(body),
            'xqueue_files': json.dumps({'anything': ''})
        }
        return json.dumps(content)

    def next(self, v_file: str):
        if self.index < len(self.directs):
            content = self.data_gen(v_file)
            self.index += 1
            return content
        return None

    def curr(self, v_file: str):
        return self.data_gen(v_file) if self.index < len(self.directs) else None

    def to_start(self):
        self.index = 0


if __name__ == '__main__':
    test = Tests('tests')
    # test = Tests('tests', 'localhost:18040')
    while True:
        data = test.next('window.mp4')
        if data is None:
            break
        print(data)
