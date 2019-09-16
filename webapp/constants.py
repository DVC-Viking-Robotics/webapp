from collections import namedtuple

Route = namedtuple('Route', 'title link');

ALL_ROUTES = [
    Route("Home",               "home"),
    Route("Remote Control",     "remote"),
    Route("Camera Feed",        "camera"),
    Route("Sensor Dashboard",   "sensors"),
    Route("Autonomous Mode",    "automode"),
    Route("Terminal I/O",       "terminal"),
    Route("Settings",           "settings"),
    Route("About",              "about"),
]