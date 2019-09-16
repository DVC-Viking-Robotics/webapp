from collections import namedtuple

Page = namedtuple('Page', 'title route metapage rowLocation id description image');

# The last 4 fields don't need explicit values if 'metapage' is True
Page.__new__.__defaults__ = ('', '', '', -1);

NUM_ROWS = 2

ALL_PAGES = [
    Page(
        title="Home",
        route="home",
        metapage=True
    ),
    Page(
        title="Remote Control",
        route="remote",
        metapage=False,
        rowLocation=0,
        id="remote-control",
        description="Control the robot remotely!",
        image="joystick"
    ),
    Page(
        title="Camera Feed",
        route="camera",
        metapage=False,
        rowLocation=0,
        id="camera",
        description="Access the robot's camera feed!",
        image="camera"
    ),
    Page(
        title="Sensor Dashboard",
        route="sensors",
        metapage=False,
        rowLocation=0,
        id="sensor-dashboard",
        description="View the robot's sensor data!",
        image="dashboard"
    ),
    Page(
        title="Autonomous Mode",
        route="automode",
        metapage=False,
        rowLocation=1,
        id="automode",
        description="Manage the robot's autonomous capabilities!",
        image="smart-brain"
    ),
    Page(
        title="Terminal I/O",
        route="terminal",
        metapage=False,
        rowLocation=1,
        id="terminal-io",
        description="Access the robot's terminal remotely!",
        image="dev-computer"
    ),
    Page(
        title="Settings",
        route="settings",
        metapage=False,
        rowLocation=1,
        id="settings",
        description="Configure the robot's settings!",
        image="settings"
    ),
    Page(
        title="About",
        route="about",
        metapage=True
    )
]