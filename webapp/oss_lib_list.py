from collections import namedtuple

Library = namedtuple('Library', 'name description link')

OSS_SERVER_LIST = [
    Library(
        'CircuitPython: NRF24L01',
        'CircuitPython driver library for the nRF24L01 transceiver.',
        'https://github.com/2bndy5/CircuitPython_nRF24L01',
    ),
    Library(
        'CircuitPython: LSM9DS1',
        'CircuitPython module for the LSM9DS1 accelerometer, magnetometer, and gyroscope.',
        'https://github.com/2bndy5/Adafruit_CircuitPython_LSM9DS1',
    ),
    Library(
        'CircuitPython: MPU6050',
        'A port of the python library for the MPU6050. 6 Degrees of Freedom sensor to CircuitPython using the Adafruit_BusDevice library.',
        'https://github.com/2bndy5/CircuitPython_MPU6050',
    ),
    Library(
        'Viking Robotics: Drivetrain',
        'This module contains the necessary algorithms for utilizing different DC motor types in different configurations.',
        'https://github.com/DVC-Viking-Robotics/Drivetrain',
    ),
    Library(
        'Viking Robotics: GPS_Serial',
        'Yet another NMEA sentence parser for serial UART based GPS modules.',
        'https://github.com/DVC-Viking-Robotics/GPS_Serial'
    ),
    Library(
        'OpenCV',
        'Open Source Computer Vision Library.',
        'https://github.com/opencv/opencv',
    ),
    Library(
        'Flask',
        'The Python micro framework for building web applications.',
        'https://github.com/pallets/flask',
    ),
    Library(
        'Flask-SocketIO',
        'Socket.IO integration for Flask applications.',
        'https://github.com/miguelgrinberg/Flask-SocketIO',
    ),
    Library(
        'Flask-CacheBuster',
        'Flask-CacheBuster is a lightweight Flask extension that adds a hash to the URL query parameters of each static file.',
        'https://github.com/israel-fl/Flask-CacheBust',
    ),
    Library(
        'Flask-Compress',
        'Compress responses in your Flask app with gzip.',
        'https://github.com/colour-science/flask-compress',
    ),
    Library(
        'Flask-Login',
        'Flask user session management.',
        'https://github.com/maxcountryman/flask-login',
    ),
    Library(
        'eventlet',
        'Concurrent networking library for Python.',
        'https://github.com/eventlet/eventlet'
    ),
    Library(
        'PySerial',
        'Python serial port access library.',
        'https://github.com/pyserial/pyserial'
    ),
]

OSS_CLIENT_LIST = [
    Library(
        'Bulma',
        'Modern CSS framework based on Flexbox.',
        'https://github.com/jgthms/bulma',
    ),
    Library(
        'Bulma Badge',
        'Bulma extension element to display a number badge on text, button, etc.',
        'https://github.com/Wikiki/bulma-badge',
    ),
    Library(
        'Bulma Divider',
        'Bulma extension to easily display an horizontal or vertical divider.',
        'https://github.com/Wikiki/bulma-divider',
    ),
    Library(
        'Bulma QuickView',
        'Bulma extension to display a QuickView compoment.',
        'https://github.com/Wikiki/bulma-quickview',
    ),
    Library(
        'Bulma Slider',
        'https://github.com/Wikiki/bulma-slider',
        'Bulma extension to display sliders.',
    ),
    Library(
        'Bulmaswatch',
        'Free themes for Bulma.',
        'https://github.com/jenil/bulmaswatch',
    ),
    Library(
        'Chart.js',
        'Simple HTML5 Charts using the <canvas> tag.',
        'https://github.com/chartjs/Chart.js',
    ),
    Library(
        'xterm.js',
        'A terminal for the web.',
        'https://github.com/xtermjs/xterm.js',
    ),
    Library(
        'outdated-browser-rework',
        'Detects outdated browsers and advises users to upgrade to a new version. Handles mobile devices!',
        'https://github.com/mikemaccana/outdated-browser-rework',
    ),
    Library(
        'ResizeSensor',
        'Javascript performance friendly element resize detection.',
        'https://github.com/procurios/ResizeSensor',
    ),
]