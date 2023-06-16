from analyzer.screencast import screencast
from analyzer.webcam import webcam
from assets.config import WINDOW_QUEUE, WEBCAM_QUEUE


HANDLERS = {
    WINDOW_QUEUE: screencast,
    WEBCAM_QUEUE: webcam
}

QUEUE_TO_NAME = {
    WINDOW_QUEUE: 'Window',
    WEBCAM_QUEUE: 'Camera'
}
