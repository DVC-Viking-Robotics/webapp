"""
This module provides an abstraction for managing cameras.
"""

# pylint: disable=relative-beyond-top-level

try:
    import cStringIO as io
except ImportError:
    import io

from .check_platform import ON_RASPI

CAMERA_AVAILABLE = False

# Import the proper libraries depending on platform
if ON_RASPI:
    try:
        import picamera
        CAMERA_AVAILABLE = True
    except ImportError:
        print('Warning: picamera is not installed')
else:  # running on a PC
    try:
        import cv2
        CAMERA_AVAILABLE = True
    except ImportError:
        print('Warning: opencv-python is not installed')
        CAMERA_AVAILABLE = False

class CameraManager:
    """ This class is for abstracting the camera feed capabilities. """

    def __init__(self):
        self.camera = None

    @property
    def initialized(self):
        """ Returns true if the camera is ready to be used """
        return CAMERA_AVAILABLE and self.camera is not None

    def _init_cv2_camera(self):
        """ Initialize the camera feed using OpenCV's implementation """
        camera = cv2.VideoCapture(0)
        return camera

    def _init_pi_camera(self):
        """ Initialize the camera feed using PiCamera's implementation """
        camera = picamera.PiCamera()
        camera.resolution = (256, 144)
        camera.start_preview(fullscreen=False, window=(100, 20, 650, 480))
        # time.sleep(1)
        # camera.stop_preview()
        return camera

    def open_camera(self):
        """ Opens and initializes the camera """
        if not CAMERA_AVAILABLE:
            raise RuntimeError('The camera is not available for use!')

        if ON_RASPI:
            try:
                self.camera = self._init_pi_camera()
            except picamera.exc.PiCameraError as picam_error:
                self.camera = None
                print('Error: picamera is not connected!')
                print(picam_error)
        else:  # running on a PC
            try:
                self.camera = self._init_cv2_camera()
            except cv2.error as cv2_error:
                self.camera = None
                print("OpenCV Error:", cv2_error)

    def capture_image(self):
        """ Fetches an image from the camera feed and incodes it as a JPEG buffer """
        if self.initialized:
            if ON_RASPI:
                sio = io.BytesIO()
                self.camera.capture(sio, "jpeg", use_video_port=True)
                buffer = sio.getvalue()
            else:
                _, frame = self.camera.read()
                _, buffer = cv2.imencode('.jpg', frame)

            return buffer
        else:
            raise RuntimeError('Camera manager is not initialized!')

    def close_camera(self):
        """
        Cleans up and closes the camera. Note that you cannot use the camera unless you
        re-initialize it with `open_camera()`
        """
        if self.initialized:
            if ON_RASPI:    # Using PiCamera
                self.camera.close()
            else:           # Using OpenCV
                self.camera.release()
        self.camera = None
