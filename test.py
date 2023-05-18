import json
import glob


class Tests:
    def __init__(self, test_path: str, host_port: str, queue_type: str):
        self.index = 0
        self.host_port = host_port
        self.queue_type = queue_type
        self.directs = sorted(glob.glob(test_path + '/*'))

    def data_gen(self):
        x_header = {
            'submission_id': str(self.index),
            'submission_key': str(self.index)
        }
        x_body = {
            'token': str(self.index),
            'data': {
                'student_data': [
                    f'http://{self.host_port}/tests/{self.directs[self.index]}/data/{self.index}'
                ],
                'student_info': [
                    f'http://{self.host_port}/tests/{self.directs[self.index]}/data/{self.index}'
                ]
            }
        }
        data = {
            'xqueue_header': json.dumps(x_header),
            'xqueue_body': json.dumps(x_body),
            'xqueue_files': json.dumps({'anything': ''})
        }
        return json.dumps(data)

    def next(self):
        if self.index < len(self.directs):
            self.index += 1
            return self.data_gen()
        return None

    def curr(self):
        return self.data_gen() if self.index != len(self.directs) else None

    def start(self):
        self.index = 0
        return self.directs[0]


if __name__ == '__main__':
    test = Tests('tests', 'localhost:18040', 'screencast')
    print(test.curr())
    while test.next() is not None:
        print(test.curr())
