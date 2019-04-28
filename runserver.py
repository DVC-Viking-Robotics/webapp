"""
This script runs the flask_controller application using a development server.
"""

try:
    import cStringIO as io
except ImportError:
    import io

import time
import base64
import os
from flask import Flask, g, render_template
from flask_socketio import SocketIO, emit
# Allow secure connections

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, logger=False, engineio_logger=False, async_mode='eventlet')

from inputs.GPSserial import GPSserial
from inputs.cmdArgs import args
cmd = args()
if cmd.getboolean('WhoAmI', 'onRaspi'):
    if cmd['Drivetrain']['interface'] == 'gpio':
        if int(cmd['Drivetrain']['motorConfig']) == 1:
            # for R2D2 configuration
            from outputs.Drivetrain import BiPed as drivetrain
        elif int(cmd['Drivetrain']['motorConfig']) == 0:
            # for race car configuration
            from outputs.Drivetrain import QuadPed as drivetrain
        pins = cmd['Drivetrain']['address'].rsplit(',')
        for i in range(len(pins)):
            pins[i] = int(pins[i])
        d = drivetrain(pins, cmd.getboolean('Drivetrain', 'phasedM'))

    # add distance sensors here using gpiozero.mcp3008 for ADC IC and gpiozero.DistanceSensor for HC-SR04 sensors
    if cmd['IMU']['interface'] == 'i2c':
        if int(cmd['IMU']['dof']) == 6:
            from inputs.IMU import MPU6050 as imu # for 6oF (GY-521)
        elif int(cmd['IMU']['dof']) == 9:
            from inputs.IMU import LSM9DS1 as imu # for 9oF (LSM9DS1)
        # IMUsensor = imu()
        IMUsensor = imu(address = cmd['IMU']['address'].rsplit(','))
    #camera dependencies
    try:
        import picamera
        camera = picamera.PiCamera()
        camera.resolution = (256, 144)
        camera.start_preview(fullscreen=False, window=(100, 20, 650, 480))
        #sleep(1)
        #camera.stop_preview()
    except picamera.exc.PiCameraError:
        camera = None
        print('picamera is not connected')
    except ImportError:
        try:
            import cv2
            camera = cv2.VideoCapture(0)
        except ImportError:
            camera = None
            print('opencv-python is not installed')
        finally:
            print('picamera is not installed')

else: # running on a PC
    try:
        import cv2
        camera = cv2.VideoCapture(0)
    except ImportError:
        print('opencv-python is not installed')
        camera = None
    
if cmd['Drivetrain']['interface'] == 'serial':
    import serial
    d = serial.Serial('/dev/ttyUSB0', 115200)

if cmd['GPS']['interface'] == 'serial':
    gps = GPSserial(cmd['GPS']['address'])
else: gps = None

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@socketio.on('webcam')
def handle_webcam_request():
    if camera != None:
        if cmd.getboolean('WhoAmI', 'onRaspi'):
            sio = io.BytesIO()
            camera.capture(sio, "jpeg", use_video_port=True)
            buffer = sio.getvalue()
        else:
            _, frame = camera.read()
            _, buffer = cv2.imencode('.jpg', frame)

        b64 = base64.b64encode(buffer)
        print('webcam buffer in bytes:', len(b64))
        emit('webcam-response', base64.b64encode(buffer))

@socketio.on('gps')
def handle_gps_request():
    print('gps data sent')
    NESW = (0,0)
    if gps != None:
        gps.getData()
        NESW = (gps.NS, gps.EW)
    else:
        NESW = (37.967135, -122.071210)
    emit('gps-response', [NESW[0], NESW[1]])

def getHYPR():
    heading = IMUsensor.calcHeading()
    YPR = IMUsensor.calcYawPitchRoll()
    print('heading:', heading, 'yaw:', YPR[0], 'pitch:', YPR[1], 'roll:', YPR[2])
    return [heading, YPR[0], YPR[1], YPR[2]]

def getIMU():
    '''
    senses[0] = accel[x,y,z]
    senses[1] = gyro[x,y,z]
    senses[2] = mag[x,y,z]
    '''
    if (cmd.getboolean('WhoAmI', 'onRaspi')) and int(cmd['IMU']['dof']) != 0:
        return IMUsensor.get_all_data()
    else:
        return [[0,0,0], [0,0,0], [0,0,0]]


@socketio.on('sensorDoF')
def handle_DoF_request():
    senses = getIMU()
    if cmd.getboolean('WhoAmI', 'onRaspi') and int(cmd['IMU']['dof']) == 9:
        emit('sensorDoF-response', [senses, getHYPR()])
    else:
        emit('sensorDoF-response', senses)
    print('DoF sensor data sent')

@socketio.on('remoteOut')
def handle_remoteOut(args):
    if cmd['Drivetrain']['interface'] == 'serial':
        command = 'Driv ' + repr(args[0]) + ' ' + repr(args[1])
        command = bytes(command.encode('utf-8'))
        d.write(command)
    elif cmd.getboolean('WhoAmI', 'onRaspi') and cmd['Drivetrain']['interface'] == 'gpio':
        d.go(args[0], args[1])
    print('remote =', repr(args))

@app.route('/')
@app.route('/remote')
def remote():
    """Renders the remote control page."""
    return render_template(
        'remote.html',
        title='Remote Control')

@app.route('/extras')
def extras():
    """Renders the features page."""
    return render_template(
        'extras.html',
        title='Extra Features',
        message='Try our more advanced features!'
    )

@app.route('/vidFeed')
def vidFeed():
    """Renders the camera page."""
    return render_template(
        'vidFeed.html',
        title='Live Camera feed',
        message='straight from the Robot!'
    )

@app.route('/automode')
def automode():
    """Google maps API with coordinate selection for auto mode."""
    return render_template(
        'automode.html',
        title='Autonomous Navigation',
        message='Autonomous Nav Mode'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About this project:',
        message='This Web App is meant to control a robot powered by Raspberry Pi via WiFi or LAN. '
    )

if __name__ == '__main__':
    try:
        socketio.run(app, host=cmd['WhoAmI']['host'], port=int(cmd['WhoAmI']['port']), debug=False)
    except KeyboardInterrupt:
        pass

