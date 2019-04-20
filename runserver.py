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
if cmd.on_raspi:
    if cmd.driveT[0] == 1:
        # for R2D2 configuration
        from outputs.Drivetrain import BiPed as drivetrain
        d = drivetrain(cmd.driveT[1], cmd.driveT[2], cmd.driveT[3], cmd.driveT[4], cmd.phasedM) # True = PMW + direction pins; False (default) = 2 PWM pins
    elif cmd.driveT[0] == 0:
        # for race car configuration
        from outputs.Drivetrain import QuadPed as drivetrain
        d = drivetrain(cmd.driveT[1], cmd.driveT[2], cmd.driveT[3], cmd.driveT[4], cmd.phasedM) # True = PMW + direction pins; False (default) = 2 PWM pins
    elif cmd.driveT[0] == 2:
        import serial
        d = serial.Serial('/dev/ttyUSB0', 115200)

    # add distance sensors here using gpiozero.mcp3008 for ADC IC and gpiozero.DistanceSensor for HC-SR04 sensors
    from inputs.mpu6050 import mpu6050 # for 6oF (GY-521)
    from inputs.LSM9DS1 import LSM9DS1 # for 9oF (LSM9DS1)
    if len(cmd.DoF) > 1:
        if cmd.DoF[0] == 9:
            IMUsensor = LSM9DS1((cmd.DoF[1:]))
    else:
        if cmd.DoF[0] == 6:
            IMUsensor = mpu6050()
        elif cmd.DoF[0] == 9:
            IMUsensor = LSM9DS1()
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
    if cmd.driveT[0] == 2:
        import serial
        d = serial.Serial('/dev/ttyUSB0', 115200)

if cmd.gps_conf[0] == 'serial':
    gps = GPSserial(cmd.gps_conf[1])
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
        if cmd.on_raspi:
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

@socketio.on('sensorDoF')
def handle_DoF_request():
    if (cmd.on_raspi):
        if cmd.DoF[0] == 6:
            accel = IMUsensor.get_accel_data()
            gyro = IMUsensor.get_gyro_data()
        if cmd.DoF[0] == 9:
            mag = IMUsensor.get_mag_data()
    else:
        accel = [0,0,0]
        gyro = [0,0,0]
        mag = [0,0,0]
    '''
    senses[0] = accel[x,y,z]
    senses[1] = gyro[x,y,z]
    senses[2] = mag[x,y,z]
    '''
    if cmd.DoF[0] == 3:
        senses=[accel]
    elif cmd.DoF[0] == 6:
        senses = [accel, gyro]
    else:
        senses = [accel, gyro, mag]
    print('DoF sensor data sent')
    emit('sensorDoF-response', senses)

@socketio.on('remoteOut')
def handle_remoteOut(args):
    if cmd.driveT[0] == 3:
        command = 'Driv ' + repr(args[0]) + ' ' + repr(args[1])
        command = bytes(command.encode('utf-8'))
        d.write(command)
    elif cmd.on_raspi and cmd.driveT[0] != 3:
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
        socketio.run(app, host=cmd.host, port=cmd.port, debug=False)
    except KeyboardInterrupt:
        pass

