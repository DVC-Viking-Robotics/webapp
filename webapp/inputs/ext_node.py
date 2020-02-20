"""
A collection of wrapper classes that extend communication with external devices (ie arduino or another raspberry pi)
"""
from webapp.outputs.roboclaw_3 import Roboclaw

class EXTnode():
    """
    This class acts as a wrapper to pyserial module for communicating to an external USB serial device. Specifically designed for an Arduino running custom code
    """
    def __init__(self, address='/dev/ttyUSB0', baud=-1):
        import serial
        self.baud = baud
        self.heading = 0
        try:
            self.address = address
            if baud < 0:
                self.ser = serial.Serial(self.address)
            else:
                self.ser = serial.Serial(self.address, baud)
            print('Successfully opened port', address, '@', baud, 'to Arduino device')
        except serial.SerialException:
            raise ValueError('unable to open serial arduino device @ port {}'.format(self.address))

    def get_all_data(self):
        """
        use this function to capture any/all data from usb serial device.
        """
        temp = self.ser.readline().decode('utf-8')
        temp = temp.rsplit(',')
        if temp:
            self.heading = float(temp[0])
        return self.heading

class ROBOCLAW:
    def __init__(self, address, claw_address=0x80):
        self._address = claw_address
        self._device = Roboclaw(address, 38400)
        self._device.Open()

    def go(self, cmds):
        if len(cmds) < 2:
            raise ValueError('Commands list needs to be atleast 2 items long')
        cmds[0] = max(-65535, min(65535, cmds[0]))
        cmds[1] = max(-65535, min(65535, cmds[1]))
        left = cmds[1]
        right = cmds[1]
        if not cmds[1]:
            # if forward/backward axis is null ("turning on a dime" functionality)
            # re-apply speed governor to only axis with a non-zero value
            right = cmds[0]
            left = cmds[0] * -1
        else:
            # if forward/backward axis is not null and left/right axis is not null
            # apply differential to motors accordingly
            offset = (65535 - abs(cmds[0])) / 65535.0
            if cmds[0] > 0:
                right *= offset
            elif cmds[0] < 0:
                left *= offset
        # send translated commands to motors
        self._device.ForwardBackwardM1(self._address, int(left * 127 / 131070 + 64))
        self._device.ForwardBackwardM2(self._address, int(right * 127 / 131070 + 64))
