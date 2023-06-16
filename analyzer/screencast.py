import os
import json


def screencast(test_path, result):
    exp_path = f'{test_path}/{result["index"]}/res/exp_window.json'
    if os.path.exists(exp_path):
        with open(exp_path, 'r') as f:
            exp = json.load(f)
            grade, grade_max = 0, len(exp['result'].keys())
            if exp['msg'] == result['answer']['msg']:
                for i in exp['result'].keys():
                    grade = grade + 1 if exp['result'][i] != result['answer']['result'][i] else grade
            return {'index': result['index'], 'result': grade / grade_max, 'time': result['answer']['elapsed_time']}
    return {'index': result['index'], 'result': 0, 'time': 0}
