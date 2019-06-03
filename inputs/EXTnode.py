
class EXTnode():
    def __init__(self, address = '/dev/ttyUSB0', baud = -1):
        import serial
        self.baud = baud
        self.heading = 0
        try:
            self.address = address
            if baud < 0:
                self.ser = serial.Serial(self.address)
            else:
                self.ser = serial.Serial(self.address, baud)
            self.dummy = False
            print('Successfully opened port', address, '@', baud, 'to Arduino device')
        except serial.SerialException:
            self.dummy = True
            print('unable to open serial arduino device @ port', self.address)

    def get_all_data(self):
        if self.dummy: # attempt to reconnect
            self.__init__(self.address, self.baud)
            if self.dummy: return 0.0 # if failed
            else: return self.get_all_data() # if success, re-call this function
        else:
            temp = self.ser.readline().decode('utf-8')
            temp = temp.rsplit(',')
            if len(temp) > 0:
                self.heading = float(temp[0])
            return self.heading

    def go(self, cmd):
        if not self.dummy:
            command = ' '
            for c in cmd:
                command += repr(c) + ' '
            print('go command =', command)
            command = bytes(command.encode('utf-8'))
            self.ser.write(command)
