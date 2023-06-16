import argparse
from collector import Collector
from analyzer import Analyzer
from assets.config import TEST_PATH, WINDOW_QUEUE, WEBCAM_QUEUE


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", action='store_true', help="tests data will contain http address instead of absolute path")
    ap.add_argument("--use_only", nargs='+', type=str, help="only screencast proctoring testing")
    ap.add_argument("--runs", type=int, help="number of times all tests running")
    args = vars(ap.parse_args())

    if args['use_only'] is not None and sorted([WEBCAM_QUEUE, WINDOW_QUEUE]) == sorted(args['use_only']):
        print('Incorrect input')
        raise KeyError

    queues = args['use_only'] if args['use_only'] is not None else [WEBCAM_QUEUE, WINDOW_QUEUE]
    run_times = args['runs'] if args['runs'] is not None else 1
    if run_times < 1:
        print('Incorrect input')
        raise KeyError

    try:
        collector = Collector()
        collector.setup(TEST_PATH, queues, run_times, args['web'])
        analyzer = Analyzer(TEST_PATH, queues)

        results = collector.run()
        summary = analyzer.run(results)
        print(summary)
    except Exception as e:
        print('Exception: ', e)
