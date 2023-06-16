import plotly.express as px
import numpy as np
import pandas as pd
from collector.utilities import AnswerPool
from analyzer.config import HANDLERS, QUEUE_TO_NAME


class Analyzer:
    def __init__(self, test_path, queues: list[str]):
        self.test_path = test_path
        self.queues = queues
        self.summary = {}

    def prepare_data(self):
        data = []
        key = list(self.summary.keys())[0]
        for j in self.summary[key]['results']:
            data.append([j['index'], j['result']])
        return pd.DataFrame(data)

    def get_graphs(self):
        dtf = self.prepare_data()
        fig = px.histogram(dtf, x=0, y=1)
        return fig

    def get_pretty_text(self):
        text = ''
        for i in self.summary.keys():
            text += f'{QUEUE_TO_NAME[i]}:\n'
            for j in self.summary[i]['results']:
                text += f'* Test {j["index"]}:\n' \
                        f'    score: {j["result"]}\n' \
                        f'    time: {j["time"]}\n'
            text += '\n\n'
        return text

    def run(self, results: list[AnswerPool]):
        self.summary = {}

        for i in self.queues:
            temp_list = []
            temp_time = 0
            grade = 0
            for result in results:
                for j in result.get_queue_results(i):
                    temp_list.append(HANDLERS[i](self.test_path, j))
            for j in temp_list:
                temp_time += j['time']
                grade += j['result']

            self.summary.update({i: {
                'grade': grade / (len(temp_list) if len(temp_list) > 0 else 1),
                'elapsed_time': temp_time,
                'results': temp_list
            }})

        return self.summary
