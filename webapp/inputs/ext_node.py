"""
A collection of wrapper classes that extend communication with external devices (ie arduino or another raspberry pi)
"""

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
