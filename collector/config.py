import os
from assets.config import WINDOW_QUEUE, WEBCAM_QUEUE

ML_HOST = os.getenv('ML_HOST', 'localhost')
ML_PORT = int(os.getenv('ML_PORT', '8070'))
XQ_HOST = os.getenv('XQ_HOST', 'localhost')
XQ_PORT = int(os.getenv('XQ_PORT', '18030'))
XQ_USERNAME = os.getenv('XQ_USERNAME', 'ml_service')
XQ_PASSWORD = os.getenv('XQ_PASSWORD', 'ml_password')

FILE_NAME_QUEUE = {
    WINDOW_QUEUE: 'window.mp4',
    WEBCAM_QUEUE: 'webcam.mp4'
}
