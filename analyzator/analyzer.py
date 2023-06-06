import os
import json
import matplotlib.pyplot as plt
from analyzator.pools import AnswerPool


class Analyzer:
    def __init__(self, test_path):
        self.test_path = test_path
        self.webcam_data = []
        self.window_data = []

    def window(self, result):
        exp_path = f'{self.test_path}/{result["index"]}/res/exp_window.json'
        if os.path.exists(exp_path):
            with open(exp_path, 'r') as f:
                exp = json.load(f)
                grade, grade_max = 0, len(exp['result'].keys())
                if exp['msg'] == result['answer']['msg']:
                    for i in exp['result'].keys():
                        grade = grade + 1 if exp['result'][i] != result['result'][i] else grade
                return {'index': result['index'], 'result': grade / grade_max, 'time': result['answer']['elapsed_time']}
        return {'index': result['index'], 'result': 0, 'time': 0}

    def webcam(self, result):  # ToDo: make webcam analyzer
        exp_path = f'{self.test_path}/{result["index"]}/res/exp_webcam.json'
        if os.path.exists(exp_path):
            # with open(exp_path, 'r') as f:
            #     exp = json.load(f)
            pass
        return {'index': result['index'], 'result': 0, 'time': 0}

    def build_graphics(self, save_path):
        pass

    def str_summary(self, summary):  # ToDo: print summary
        return str(summary)

    def run(self, results: AnswerPool, save_path, save_summary=False):
        summary = {'window': {}, 'webcam': {}}

        temp_list = []
        temp_time = 0
        grade = 0
        for i in results.get_window_results():
            temp_list.append(self.window(i))
        for i in temp_list:
            temp_time += i['time']
            grade += i['result']

        summary['window'] = {
            'grade': grade / len(temp_list),
            'elapsed_time': temp_time,
            'results': temp_list
        }

        temp_list = []
        temp_time = 0
        grade = 0
        for i in results.get_webcam_results():
            temp_list.append(self.webcam(i))
        for i in temp_list:
            temp_time += i['time']

        summary['webcam'] = {
            'grade': grade / len(temp_list),
            'elapsed_time': temp_time,
            'results': temp_list
        }

        self.build_graphics(save_path)

        if save_summary:
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            with open(f'{save_path}/summary.txt', 'w') as f:
                f.write(self.str_summary(summary))

        return self.str_summary(summary)
