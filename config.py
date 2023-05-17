import os

ML_HOST = os.getenv('ML_HOST', '127.0.0.1')
ML_PORT = os.getenv('ML_PORT', 8080)
XQ_HOST = os.getenv('XQ_HOST', '127.0.0.1')
XQ_PORT = os.getenv('XQ_PORT', 18040)
XQ_USERNAME = os.getenv('XQ_USERNAME', 'ml_service')
XQ_PASSWORD = os.getenv('XQ_PASSWORD', 'ml_password')