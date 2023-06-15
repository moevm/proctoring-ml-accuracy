import time
import uvicorn
import threading
import collector.xqueue as xqueue
from collector.config import XQ_PORT, XQ_HOST, ML_PORT, ML_HOST
from collector.utilities import TestPool


class Collector:
    def __init__(self):
        self.tests = None
        self.run_times = 0
        self.results = None
        self.initialized = False

    def run(self):
        if not self.initialized:
            return None

        self.results = []
        for _ in range(self.run_times):
            x_server = uvicorn.Server(uvicorn.Config('xqueue:app', host=XQ_HOST, port=XQ_PORT))
            x_th = threading.Thread(target=lambda: x_server.run(), args=())
            x_th.start()

            m_server = uvicorn.Server(uvicorn.Config('moodle:app', host=ML_HOST, port=ML_PORT))
            m_th = threading.Thread(target=lambda: m_server.run(), args=())
            m_th.start()

            result = xqueue.result()
            while result is None:
                time.sleep(0.5)
                result = xqueue.result()

            self.results.append(result)
            xqueue.refresh()

            x_server.handle_exit(2, None)
            m_server.handle_exit(2, None)

            if x_th.is_alive():
                x_th.join()
            if m_th.is_alive():
                m_th.join()

        return self.results

    def get_last_results(self):
        return self.results

    def setup(self, test_path, queues: list[str], runs: int, http: bool = False):
        self.tests = TestPool(test_path)
        if http:
            self.tests.set_data_output('web', XQ_HOST + ':' + str(XQ_PORT))
        self.run_times = runs
        self.results = []
        xqueue.setup(queues, self.tests)
        self.initialized = True
