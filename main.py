from xqueue import run as x_run, test_iters, results
from moodle import run as m_run
from analyzator.analyzer import Analyzer
from config import TEST_PATH
import argparse
import time


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", action='store_true', help="tests data will contain http address instead of absolute path")
    ap.add_argument("--only_camera", action='store_true', help="only web-camera proctoring testing")
    ap.add_argument("--only_screen", action='store_true', help="only screencast proctoring testing")
    args = vars(ap.parse_args())

    xqueue = x_run(args)
    moodle = m_run(args)

    while len(test_iters.values()) != 0:
        time.sleep(0.5)

    xqueue.handle_exit(2, None)
    moodle.handle_exit(2, None)

    # Analyzing

    analyzer = Analyzer(TEST_PATH)
    summary = analyzer.run(results, './summary')
    print(summary)
