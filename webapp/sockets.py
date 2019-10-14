"""A collection of websocket routes"""
# pylint: disable=invalid-name

import base64
from flask_socketio import SocketIO, emit
from circuitpython_mpu6050 import MPU6050
from adafruit_lsm9ds1 import LSM9DS1_I2C

from .inputs.check_platform import ON_WINDOWS
from .inputs.config import d_train, IMUs, gps, nav
from .inputs.imu import MAG3110, calc_heading, calc_yaw_pitch_roll
from .inputs.camera_manager import CameraManager
from .utils.virtual_terminal import VTerminal

socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

# for virtual terminal access
if not ON_WINDOWS:
    vterm = VTerminal(socketio)
    vterm.register_output_listener(
        lambda output: socketio.emit("terminal-output", {"output": output}, namespace="/pty")
    )

# Initialize the camera
camera_manager = CameraManager()
camera_manager.open_camera()


def getHYPR():
    """HYPR = Heading Yaw Pitch Roll. This function """
    heading = []
    yaw = 0
    pitch = 0
    roll = 0
    for imu in IMUs:
        if type(imu, LSM9DS1_I2C):
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
    senses = [
        [100, 50, 25],
        [-100, -50, -25],
        [100, -50, 25]
    ]

    for imu in IMUs:
        if isinstance(imu, LSM9DS1_I2C):
            senses[0] = list(imu.acceleration)
            senses[1] = list(imu.gyro)
            senses[2] = list(imu.magnetic)
        elif isinstance(imu, MPU6050):
            senses[0] = list(imu.acceleration)
            senses[1] = list(imu.gryo)
    return senses


@socketio.on('connect')
def handle_connect():
    """This event fired when a websocket client establishes a connection to the server"""
    print('websocket Client connected!')


@socketio.on('disconnect')
def handle_disconnect():
    """This event fired when a websocket client breaks connection to the server"""
    print('websocket Client disconnected')

    # If the camera was recently opened, then close it and reopen it to free the resource for
    # future use. The reason for "rebooting" the camera is that the camera device will be
    # considered "in use" until the corresponding resource is freed, for which we can re-initialize
    # the camera resource again.
    if camera_manager.initialized:
        camera_manager.close_camera()
        camera_manager.open_camera()

    # If the vterm was initialized and/or running, close file descriptor and kill child process
    if not ON_WINDOWS:
        if vterm.running or vterm.initialized:
            vterm.cleanup()


@socketio.on('webcam')
def handle_webcam_request():
    """This event is to stream the webcam over websockets."""
    if camera_manager.initialized:
        buffer = camera_manager.capture_image()
        b64 = base64.b64encode(buffer)
        # print('webcam buffer in bytes:', len(b64))
        emit('webcam-response', b64)

@socketio.on('WaypointList')
def build_wapypoints(waypoints, clear):
    """Builds a list of waypoints based on the order they were created on
    the 'automode.html' page

    :param list waypoints: A list of GPS latitude & longitude pairs for the robot to
        travel to in sequence.

    :param bool clear: A flag that will clear the eisting list of GPS waypoints before appending to
        it.

    """
    if nav is not None:
        if clear:
            nav.clear()
        print('received waypoints')
        for point in waypoints:
            nav.insert(point)
        nav.printWP()

@socketio.on('gps')
def handle_gps_request():
    """This event fired when a websocket client's response to the server about GPS coordinates."""
    print('gps data sent')
    NESW = (0, 0)
    if gps:
        gps[0].get_data()
        NESW = (gps[0].lat, gps[0].lng)
    else:
        NESW = (37.967135, -122.071210)
    emit('gps-response', [NESW[0], NESW[1]])

@socketio.on('sensorDoF')
def handle_DoF_request():
    """This event fired when a websocket client a response to the server about IMU data."""
    senses = get_imu_data()
    emit('sensorDoF-response', senses)
    print('DoF sensor data sent')

@socketio.on('remoteOut')
def handle_remoteOut(arg):
    """This evemt gets fired when the client sends data to the server about remote controls
    (via remote control page)"""
    print('remote =', repr(arg))
    if d_train: # if there is a drivetrain connected
        d_train[0].go([arg[0] * 655.35, arg[1] * 655.35])

# NOTE: Source for virtual terminal functions: https://github.com/cs01/pyxterm.js

# virtual terminal handlers
@socketio.on("terminal-input", namespace="/pty")
def on_terminal_input(data):
    """ Write to the child pty. The pty sees this as if you are typing in a real terminal. """
    if not ON_WINDOWS:
        vterm.write_input(data["input"].encode())

@socketio.on("terminal-resize", namespace="/pty")
def on_terminal_resize(data):
    """This event is fired when a websocket clients' window gets resized to the server"""
    if not ON_WINDOWS:
        vterm.resize_terminal(data["rows"], data["cols"])

@socketio.on("connect", namespace="/pty")
def on_terminal_connect():
    """ A new client has connected """
    if not ON_WINDOWS:
        vterm.init_connect(["/bin/bash", "./webapp/bash_scripts/ask_pass_before_bash.sh"])
