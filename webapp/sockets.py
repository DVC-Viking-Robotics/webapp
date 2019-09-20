
# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

try:
    import cStringIO as io
except ImportError:
    import io

import base64
from flask_socketio import SocketIO, emit
from circuitpython_mpu6050 import MPU6050
from .inputs.check_platform import is_on_raspberry_pi
from .inputs.config import d_train, IMUs, gps, nav
from .inputs.imu import LSM9DS1_I2c, MAG3110, calc_heading, calc_yaw_pitch_roll

on_raspi = is_on_raspberry_pi()
socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

# handle camera dependencies
if on_raspi:
    try:
        import picamera
        camera = picamera.PiCamera()
        camera.resolution = (256, 144)
        camera.start_preview(fullscreen=False, window=(100, 20, 650, 480))
        # time.sleep(1)
        # camera.stop_preview()
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

def getHYPR():
    heading = []
    yaw = 0
    pitch = 0
    roll = 0
    for imu in IMUs:
        if type(imu, LSM9DS1_I2c):
            heading.append(calc_heading(imu.magnetic))
            yaw, pitch, roll = calc_yaw_pitch_roll(imu.acceleration, imu.gyro)
        elif type(imu, MAG3110):
            heading.append(imu.get_heading())
    if not heading:
        heading.append(0)
    print('heading:', heading[0], 'yaw:', yaw, 'pitch:', pitch, 'roll:', roll)
    return [heading[0], yaw, pitch, roll]

def get_imu_data():
    '''
    senses[0] = accel[x,y,z]
    senses[1] = gyro[x,y,z]
    senses[2] = mag[x,y,z]
    '''
    senses = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for imu in IMUs:
        if type(imu, LSM9DS1_I2c):
            senses[0] = imu.acceleration
            senses[1] = imu.gyro
            senses[2] = imu.magnetic
        elif type(imu, MPU6050):
            senses[0] = imu.acceleration
            senses[1] = imu.gryo
    return senses

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@socketio.on('webcam')
def handle_webcam_request():
    if camera is not None:
        if on_raspi:
            sio = io.BytesIO()
            camera.capture(sio, "jpeg", use_video_port=True)
            buffer = sio.getvalue()
        else:
            _, frame = camera.read()
            _, buffer = cv2.imencode('.jpg', frame)

        b64 = base64.b64encode(buffer)
        print('webcam buffer in bytes:', len(b64))
        emit('webcam-response', b64)

@socketio.on('WaypointList')
def build_wapypoints(waypoints, clear):
    if nav is not None:
        if clear:
            nav.clear()
        print('received waypoints')
        for point in waypoints:
            nav.insert(point)
        nav.printWP()

@socketio.on('gps')
def handle_gps_request():
    print('gps data sent')
    NESW = (0, 0)
    if gps is not None:
        gps.get_data()
        NESW = (gps.lat, gps.lng)
    else:
        NESW = (37.967135, -122.071210)
    emit('gps-response', [NESW[0], NESW[1]])

@socketio.on('sensorDoF')
def handle_DoF_request():
    senses = get_imu_data()
    emit('sensorDoF-response', senses)
    print('DoF sensor data sent')

@socketio.on('remoteOut')
def handle_remoteOut(arg):
    # for debugging
    print('remote =', repr(arg))
    if d_train: # if there is a drivetrain connected
        d_train[0].go([arg[0], arg[1]])
