"""
A collection of wrapper classes that extend communication with external devices (ie arduino or another raspberry pi)
"""
import struct


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
            self._dummy = False
            print('Successfully opened port', address,
                  '@', baud, 'to Arduino device')
        except serial.SerialException:
            self._dummy = True
            print('unable to open serial arduino device @ port', self.address)

    def get_all_data(self):
        """
        use this function to capture any/all data from usb serial device.
        """
        if self._dummy:  # attempt to reconnect
            self.__init__(self.address, self.baud)
            if self._dummy:
                return 0.0  # if failed
            return self.get_all_data()  # if success, re-call this function
        else:
            temp = self.ser.readline().decode('utf-8')
            temp = temp.rsplit(',')
            if temp:
                self.heading = float(temp[0])
            return self.heading

    def go(self, cmd):
        """ assembles a encoded bytearray for outputting on the serial connection"""
        if not self._dummy:
            command = ' '
            for c in cmd:
                command += repr(c) + ' '
            command = bytes(command.encode('utf-8'))
            self.ser.write(command)


class NRF24L01():
    """This class acts as a wrapper for circuitpython-nrf24l01 module to remotely control a peripheral device using nRF24L01 radio transceivers"""

    def __init__(self, spi, csn, ce, address=b'rfpi0'):
        from circuitpython_nrf24l01 import RF24
        self._rf = RF24(spi, csn, ce)
        self._rf.open_tx_pipe(address)
        self._rf.what_happened(1)

    def go(self, cmd):
        """Assembles a bytearray to be used for transmitting commands over the air"""
        temp = struct.pack('bb', cmd[0], cmd[1])
        print('transmit', repr(cmd), 'returned:', self._rf.send(temp))
