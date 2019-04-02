# webapp
flask implementation of remote control via wifi for robot

Required BEFORE Install:
opencv2 

picamera

Flask==1.0.2
Flask-SocketIO==3.3.1
gevent==1.4.0
gevent-websocket==0.10.1
greenlet==0.4.15
itsdangerous==1.1.0
Jinja2==2.10
MarkupSafe==1.1.1
python-engineio==3.4.3
python-socketio==3.1.2
six==1.12.0

How to install:
git clone <this repo>

How to Run:
  on a Raspberry pi:
  python3 runserver.py [cmd args]
  
  if on windows and only python V3+ is install:
  python runserver.py
