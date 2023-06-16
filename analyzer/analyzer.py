from collector.utilities import AnswerPool
from analyzer.config import HANDLERS


class Analyzer:
    def __init__(self, test_path, queues: list[str]):
        self.test_path = test_path
        self.queues = queues
        self.summary = {}

    def get_graphs_meta(self):
        pass

    def get_tests_meta(self):
        pass

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
