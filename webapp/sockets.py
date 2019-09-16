
# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

try:
    import cStringIO as io
except ImportError:
    import io

import base64
from flask_socketio import SocketIO, emit
from .inputs.cmdArgs import Args
from .inputs.ext_node import EXTnode, NRF24L01
from .GPS_Serial.gps_serial import GPSserial

cmd = Args()
socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

# handle camera dependencies
if cmd.getboolean('WhoAmI', 'onRaspi'):
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

# handle drivetrain
if cmd.getboolean('WhoAmI', 'onRaspi') and cmd['Drivetrain']['interface'] == 'gpio':
    if int(cmd['Drivetrain']['motorConfig']) == 1:
        # for R2D2 configuration
        from .Drivetrain.drivetrain.drivetrain import BiPed as dtrain
    elif int(cmd['Drivetrain']['motorConfig']) == 0:
        # for race car configuration
        from .Drivetrain.drivetrain.drivetrain import QuadPed as dtrain
    pins = cmd['Drivetrain']['address'].rsplit(':')
    for i, p in enumerate(pins):
        p = p.rsplit(',')
        for j, pin in enumerate(p):
            pin = int(pin)
    print('drivetrain pins:', repr(pins))
    d = dtrain(pins, cmd['Drivetrain']['phasedM'], int(cmd['Drivetrain']['maxSpeed']))
elif cmd['Drivetrain']['interface'] == 'serial':
    d = EXTnode(cmd['Drivetrain']['address'], int(cmd['Drivetrain']['baud']))
elif cmd.getboolean('WhoAmI', 'onRaspi') and cmd['Drivetrain']['interface'] == 'spi':
    import board
    import digitalio as dio
    d = NRF24L01(board.SPI(), dio.DigitalInOut(board.D5), dio.DigitalInOut(board.CE0))
else: d = None

if cmd['IMU']['interface'] == cmd['Drivetrain']['interface']:
    IMUsensor = d
elif cmd['IMU']['interface'] == 'serial':
    IMUsensor = EXTnode(cmd['IMU']['address'], int(cmd['IMU']['baud']))
elif cmd.getboolean('WhoAmI', 'onRaspi') and cmd['IMU']['interface'] == 'i2c':
    if int(cmd['IMU']['dof']) == 6:
        from .inputs.IMU import MPU6050 as imu # for 6oF (GY-521)
    elif int(cmd['IMU']['dof']) == 9:
        from .inputs.IMU import LSM9DS1 as imu # for 9oF (LSM9DS1)
    # IMUsensor = imu()
    IMUsensor = imu(address=cmd['IMU']['address'].rsplit(','))
else: IMUsensor = None

if cmd['GPS']['interface'] == 'serial':
    gps = GPSserial(cmd['GPS']['address'])
else: gps = None

if gps is not None and IMUsensor is not None:
    from .outputs.GPSnav import GPSnav
    nav = GPSnav(d, IMUsensor, gps)
else: nav = None

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
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@socketio.on('webcam')
def handle_webcam_request():
    if camera is not None:
        if cmd.getboolean('WhoAmI', 'onRaspi'):
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
    senses = getIMU()
    if cmd.getboolean('WhoAmI', 'onRaspi') and int(cmd['IMU']['dof']) == 9:
        emit('sensorDoF-response', [senses, getHYPR()])
    else:
        emit('sensorDoF-response', senses)
    print('DoF sensor data sent')

@socketio.on('remoteOut')
def handle_remoteOut(arg):
    # for debugging
    print('remote =', repr(arg))
    if d: # if there is a drivetrain connected
        d.go([arg[0], arg[1]])
