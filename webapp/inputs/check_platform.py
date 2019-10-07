"""A module that uses Adafruit-PlatformDetect for detecting hardware and OS conditions.
This module will contain the following information:

    * ON_WINDOWS (`bool`) `True` if Windows OS is detected, otherwise `False`
    * ON_RASPI (`bool`) `True` if raspberry pi is detected, otherwise `False`
    * ON_JETSON (`bool`) `True` if nVidia Jetson is detected, otherwise `False`

We could add more here. For a complete list of names for devices that CircuitPython will
aggree with (not Windows), the following commands in a Python REPR:

.. code-block:: python

    >>> import adafruit_platformdetect
    >>> dir(adafruit_platformdetect.board)
    ['BEAGLEBONE', 'BEAGLEBONE_AIR', 'BEAGLEBONE_BLACK', 'BEAGLEBONE_BLACK_INDUSTRIAL', 'BEAGLEBONE_BLACK_WIRELESS', 'BEAGLEBONE_BLUE', 'BEAGLEBONE_ENHANCED', 'BEAGLEBONE_GREEN', 'BEAGLEBONE_GREEN_WIRELESS', 'BEAGLEBONE_POCKETBEAGLE', 'BEAGLEBONE_POCKETBONE', 'BEAGLEBONE_USOMIQ', 'BEAGLELOGIC_STANDALONE', 'Board', 'CORAL_EDGE_TPU_DEV', 'DRAGONBOARD_410C', 'FEATHER_HUZZAH', 'FEATHER_M0_EXPRESS', 'FTDI_FT232H', 'GENERIC_LINUX_PC', 'GIANT_BOARD', 'JETSON_NANO', 'JETSON_TX1', 'JETSON_TX2', 'JETSON_XAVIER', 'NODEMCU', 'ODROID_C1', 'ODROID_C1_PLUS', 'ODROID_C2', 'ODROID_N2', 'ORANGE_PI_PC', 'ORANGE_PI_R1', 'ORANGE_PI_ZERO', 'OSD3358_DEV_BOARD', 'OSD3358_SM_RED', 'PYBOARD', 'RASPBERRY_PI_2B', 'RASPBERRY_PI_3A_PLUS', 'RASPBERRY_PI_3B', 'RASPBERRY_PI_3B_PLUS', 'RASPBERRY_PI_4B', 'RASPBERRY_PI_A', 'RASPBERRY_PI_A_PLUS', 'RASPBERRY_PI_B_PLUS', 'RASPBERRY_PI_B_REV1', 'RASPBERRY_PI_B_REV2', 'RASPBERRY_PI_CM1', 'RASPBERRY_PI_CM3', 'RASPBERRY_PI_CM3_PLUS', 'RASPBERRY_PI_ZERO', 'RASPBERRY_PI_ZERO_W', 'SIFIVE_UNLEASHED', '_BEAGLEBONE_BOARD_IDS', '_BEAGLEBONE_IDS', '_CORAL_IDS', '_JETSON_IDS', '_LINARO_96BOARDS_IDS', '_ODROID_40_PIN_IDS', '_ORANGE_PI_IDS', '_PI_REV_CODES', '_RASPBERRY_PI_40_PIN_IDS', '_RASPBERRY_PI_CM_IDS', '_SIFIVE_IDS', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'ap_chip', 'os']

"""
import adafruit_platformdetect as pfdetect

ON_WINDOWS = pfdetect.platform.platform(aliased=1, terse=1).startswith('Windows')

DETECT = pfdetect.Detector()  # object used to detect various information
MODEL = DETECT.board.id       # returns `None` on Windows

ON_RASPI = False if MODEL is None else MODEL.startswith('RASPBERRY_PI')
ON_JETSON = False if MODEL is None else MODEL.startswith('JETSON')
