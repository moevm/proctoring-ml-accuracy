import os

ML_HOST = os.getenv('ML_HOST', 'localhost')
ML_PORT = int(os.getenv('ML_PORT', '8080'))
XQ_HOST = os.getenv('XQ_HOST', 'localhost')
XQ_PORT = int(os.getenv('XQ_PORT', '18040'))
XQ_USERNAME = os.getenv('XQ_USERNAME', 'ml_service')
XQ_PASSWORD = os.getenv('XQ_PASSWORD', 'ml_password')

TEST_PATH = 'tests'

WINDOW_QUEUE = 'screencast_queue'
WEBCAM_QUEUE = 'webcam_queue'
FILE_NAME_QUEUE = {
    'screencast_queue': 'window.mp4',
    'webcam_queue': 'webcam.mp4'
}
