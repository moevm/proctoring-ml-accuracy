import os
import json


def webcam(test_path, result):
    exp_path = f'{test_path}/{result["index"]}/res/exp_webcam.json'
    if os.path.exists(exp_path):
        with open(exp_path, 'r') as f:
            exp = json.load(f)
            grade, grade_max = 0, len(exp['result'].keys())
            if exp['msg'] == result['answer']['msg']:
                grade = grade_max
                return {'index': result['index'], 'result': grade / grade_max, 'time': result['answer']['elapsed_time']}
    return {'index': result['index'], 'result': 0, 'time': 0}
