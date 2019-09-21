
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

# for virtual terminal access
import pty
import os
import subprocess
import select       # async I/O for file descriptors; used for retrieving terminal output
import termios      # used to set the window size (look up "TIOCSWINSZ" in https://linux.die.net/man/4/tty_ioctl)
import struct       # struct library used for packing data for setting terminal window size
import fcntl        # I/O for file descriptors; used for setting terminal window size
import shlex        # used to shell-escape commands to prevent unsafe multi-commands (like "ls -l somefile; rm -rf ~")

fd = None
child_pid = None
term_cmd = ["bash"]

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
    if len(gps) > 0:
        # TODO: Figure out how to handle multiple GPS readings
        gps[0].get_data()
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

# NOTE: Source for virtual terminal functions: https://github.com/cs01/pyxterm.js

# virtual terminal handlers
@socketio.on("terminal-input", namespace="/pty")
def on_terminal_input(data):
    global child_pid, fd, term_cmd
    """write to the child pty. The pty sees this as if you are typing in a real terminal."""
    if fd:
        # print("writing to ptd: %s" % data["input"])
        os.write(fd, data["input"].encode())


@socketio.on("terminal-resize", namespace="/pty")
def on_terminal_resize(data):
    global fd
    if fd:
        set_winsize(fd, data["rows"], data["cols"])


@socketio.on("connect", namespace="/pty")
def on_terminal_connect():
    global child_pid, fd, term_cmd
    """new client connected"""

    if child_pid:
        # already started child process, don't start another
        return

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run(term_cmd)
    else:
        # this is the parent process fork.
        set_winsize(fd, 50, 50)
        term_cmd = " ".join(shlex.quote(c) for c in term_cmd)
        print("child pid is", child_pid)
        print(
            f"starting background task with command `{term_cmd}` to continously read "
            "and forward pty output to client"
        )
        socketio.start_background_task(target=read_and_forward_pty_output)
        print("task started")


# virtual terminal helper functions
def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output():
    global fd
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select([fd], [], [], timeout_sec)
            if data_ready:
                # for invalid characters, print out the hex representation
                output = os.read(fd, max_read_bytes).decode(encoding='utf-8', errors='backslashreplace')
                socketio.emit("terminal-output", {"output": output}, namespace="/pty")