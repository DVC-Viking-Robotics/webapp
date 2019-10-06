
# to temporarily disable non-crucial pylint errors in conformity
# pylint: disable=invalid-name,missing-docstring

import os
import subprocess
import base64
import struct       # struct library to pack data into bytearrays for setting terminal window size
import select       # async I/O for file descriptors; used for retrieving terminal output
import shlex        # used to shell-escape commands to prevent unsafe multi-commands (like "ls -l somefile; rm -rf ~")
from flask_socketio import SocketIO, emit
from circuitpython_mpu6050 import MPU6050
from adafruit_lsm9ds1 import LSM9DS1_I2C
# pylint: disable=import-error,wrong-import-position
from .inputs.check_platform import ON_RASPI, ON_WINDOWS  # , ON_JETSON
if not ON_WINDOWS:
    import pty          # docs @ https://docs.python.org/3/library/pty.html
    import termios      # used to set the window size (look up "TIOCSWINSZ" in https://linux.die.net/man/4/tty_ioctl)
    import fcntl        # I/O for file descriptors; used for setting terminal window size
# pylint: enable=import-error
from .inputs.config import d_train, IMUs, gps, nav
from .inputs.imu import MAG3110, calc_heading, calc_yaw_pitch_roll

from .inputs.camera_manager import CameraManager

# for virtual terminal access
fd = None           # This stands for "file descriptor" used as an I/O handle
child_pid = None    # The child process ID; used to avoid starting multiple processes for the same task
term_cmd = ["bash"]

socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

# Initialize the camera
camera_manager = CameraManager()
camera_manager.open_camera()


def getHYPR():
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
    print('websocket Client connected!')


@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

    # If the camera was recently opened, then close it and reopen it to free the resource for future use
    # The reason for "rebooting" the camera is that the camera device will be considered "in use" until
    # the corresponding resource is freed, for which we can re-initialize the camera resource again.
    if camera_manager.initialized:
        camera_manager.close_camera()
        camera_manager.open_camera()


@socketio.on('webcam')
def handle_webcam_request():
    if camera_manager.initialized:
        buffer = camera_manager.capture_image()
        b64 = base64.b64encode(buffer)
        # print('webcam buffer in bytes:', len(b64))
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
    if gps:
        gps[0].get_data()
        NESW = (gps[0].lat, gps[0].lng)
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
        d_train[0].go([arg[0] * 655.35, arg[1] * 655.35])

# NOTE: Source for virtual terminal functions: https://github.com/cs01/pyxterm.js

# virtual terminal handlers
@socketio.on("terminal-input", namespace="/pty")
def on_terminal_input(data):
    """write to the child pty. The pty sees this as if you are typing in a real terminal."""
    if not ON_WINDOWS:
        global child_pid, fd, term_cmd
        if fd:
            # print("writing to ptd: %s" % data["input"])
            os.write(fd, data["input"].encode())

@socketio.on("terminal-resize", namespace="/pty")
def on_terminal_resize(data):
    if not ON_WINDOWS:
        global fd
        if fd:
            set_winsize(fd, data["rows"], data["cols"])

@socketio.on("connect", namespace="/pty")
def on_terminal_connect():
    """new client connected"""
    if not ON_WINDOWS:
        global child_pid, fd, term_cmd

        if child_pid:
            # already started child process, don't start another
            return # maybe needed to manage multiple client sessions across 1 server

        # create child process attached to a pty we can read from and write to
        (child_pid, fd) = pty.fork() # read docs for this https://docs.python.org/3/library/pty.html#pty.fork
        # now child_pid == 0, and fd == 'invalid'
        if child_pid == 0:
            # this is the child process fork. Anything printed here will show up in the pty,
            # including the output of this subprocess
            # docs for subprocess.run @ https://docs.python.org/3/library/subprocess.html#subprocess.run
            subprocess.run(term_cmd) # term_cmd is a list of arguments that (in our case) get passed to
            # subprocess.Popen(); docs @ https://docs.python.org/3/library/subprocess.html#subprocess.Popen
            # docs say term_cmd can be a simple string which (in our case) would be a little easier as long as
            # we don't need to add more args to the `bash` program's starting call

            # NOTE `multiprocessing` module has subprocess.run() functionality abstracted into their `Process` class
        else:
            # this is the parent process fork.
            set_winsize(fd, 50, 50)
            # now concatenate the term_cmd list into a " " delimited string for
            # outputting in the debugging print() cmds. See also previous comment after Popen() docs link
            term_cmd = " ".join(shlex.quote(c) for c in term_cmd)
            print("terminal thread's Process ID is", child_pid)
            print(
                f"starting background task with command `{term_cmd}` to continously read "
                "and forward pty output to client"
            )
            # docs for start_background_task @ https://flask-socketio.readthedocs.io/en/latest/#flask_socketio.SocketIO.start_background_task
            socketio.start_background_task(target=read_and_forward_pty_output)
            # since this method returns a `threading.Thread` object that is already start()-ed, we can
            # simply capture the thread's instance for the multiprocessing module, but not until I know how
            print("thread for terminal started")

# virtual terminal helper functions
def set_winsize(fd, row, col, xpix=0, ypix=0):
    # ioctl will only accept window size parameters as a bytearray
    winsize = struct.pack("HHHH", row, col, xpix, ypix) # contruct the bytearray
    if not ON_WINDOWS:
        # NOTE: This method does *not* take keyword arguments!
        fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)
        # docs for this @ https://docs.python.org/3/library/fcntl.html#fcntl.ioctl

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
