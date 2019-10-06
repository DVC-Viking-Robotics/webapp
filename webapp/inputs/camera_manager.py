# NOTE: Module 'cv2' has no 'VideoCapture' member -- pylint(no-member)
# pylint: disable=no-member,relative-beyond-top-level

try:
    import cStringIO as io
except ImportError:
    import io

from .check_platform import ON_RASPI


camera_available = False

# Import the proper libraries depending on platform
if ON_RASPI:
    try:
        import picamera
        camera_available = True
    except ImportError:
        print('Warning: picamera is not installed')
else:  # running on a PC
    try:
        import cv2
        camera_available = True
    except ImportError:
        print('Warning: opencv-python is not installed')
        camera_available = False


# This class is for abstracting the camera feed capabilities.
class CameraManager:
    def __init__(self):
        self.camera = None

    @property
    def initialized(self):
        return camera_available and self.camera is not None

    # Initialize the camera feed using OpenCV's implementation
    def _init_cv2_camera(self):
        camera = cv2.VideoCapture(0)
        return camera

    # Initialize the camera feed using PiCamera's implementation
    def _init_pi_camera(self):
        camera = picamera.PiCamera()
        camera.resolution = (256, 144)
        camera.start_preview(fullscreen=False, window=(100, 20, 650, 480))
        # time.sleep(1)
        # camera.stop_preview()
        return camera

    # Opens and initializes the camera
    def open_camera(self):
        if not camera_available:
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
            except cv2.error as e:
                self.camera = None
                print("OpenCV Error:", e)

    # Fetches an image from the camera feed and incodes it as a JPEG buffer
    def capture_image(self):
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

    # Cleans up and closes the camera. Note that you cannot use the camera unless you
    # re-initialize it with `CameraManager.open_camera()`
    def close_camera(self):
        if self.initialized:
            if ON_RASPI:    # Using PiCamera
                self.camera.close()
            else:           # Using OpenCV
                self.camera.release()
        self.camera = None

# pylint: enable=no-member
