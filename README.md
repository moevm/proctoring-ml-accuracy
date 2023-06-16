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

For _moodle_ by default:
```
ML_HOST=http://127.0.0.1
ML_PORT=8080
```
For _xqueue_ by default:
```
XQ_HOST=http://127.0.0.1
XQ_PORT=18040
XQ_USERNAME=ml_service
XQ_PASSWORD=ml_password
```

**Run benchmarking:**

`python cli.py  [--web --only_screen --only_camera]`

CLI:

* _--web_ - this command mean tests data will contain http address instead of absolute path.
* _--only_screen_ - with this command benchmark will test only screencast proctoring.
* _--only_camera_ - with this command benchmark will test only web-camera proctoring.

**Run benchmark with Web UI:**

`python app.py`

_xqueue server_ will return tests on request 'get_submission' until they run out, 
then it will send a response with a 405 error code.

## Tests
### Test directories structure

```
tests/
├── 1/
│   ├── data/
│   │   ├── photo.jpg [.png]
│   │   ├── webcam.mp4
│   │   └── window.mp4
│   └── res/
│       ├── exp_webcam.json
│       └── exp_window.json
├── 2/
│   ├── data/
│   │   ├── photo.jpg [.png]
│   │   ├── webcam.mp4
│   │   └── window.mp4
│   └── res/
│       ├── exp_webcam.json
│       └── exp_window.json
    . . . . . . . .
└── n/
    ├── data/
    │   ├── photo.jpg [.png]
    │   ├── webcam.mp4
    │   └── window.mp4
    └── res/
        ├── exp_webcam.json
        └── exp_window.json
```

Folder structure with expected results will be done soon.

Tests folder name must be only number. Other names of folders and files in the test are not allowed.