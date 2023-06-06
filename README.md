# proctoring-ml-accuracy
## Overview
This project contains two modules - _xqueue.py_ and _moodle.py_ - that create 
an environment for testing the ml-proctoring web-service.

**Project use:** Python3.9+
## Running
### Manual run
Create virtual environment  
`python3 -m venv venv`  

Activate and install dependencies  
```
source ./venv/bin/activate
pip install -r requirements.txt
```

Setup environment variables (optionally):

For _moodle_:
```
ML_HOST=http://127.0.0.1
ML_PORT=8080
```
For _xqueue_:
```
XQ_HOST=http://127.0.0.1
XQ_PORT=18040
XQ_USERNAME=ml_service
XQ_PASSWORD=ml_password
```

Run modules:

`python xqueue.py  [--web]`

`python moodle.py`

_xqueue.py_ can optional run with _--web_ flag which mean that tests data 
will contain http address instead of absolute path.

_xqueue server_ will return tests on request 'get_submission' until they run out, 
then it will send a response with a 405 error code.

## Tests
### Test directories structure

```
tests/
├── 1
│   ├── data
│   │   ├── photo.jpg [.png]
│   │   ├── webcam.mp4
│   │   └── window.mp4
│   └── res
│       └── <some expected results>
└── 2
    ├── data
    │   ├── photo.jpg [.png]
    │   ├── webcam.mp4
    │   └── window.mp4
    └── res
        └── <some expected results>
```

Folder structure with expected results will be done soon.

Tests folder name must be only number. Other names of folders and files in the test are not allowed.