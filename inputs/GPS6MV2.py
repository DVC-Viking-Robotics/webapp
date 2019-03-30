import serial
import time

# open a "channel" (technically I think its called a "handle") to Serial port
# on Windows my arduino registers as "COM3"
# on rasbian the Tx/Rx pins register as '/dev/ttyS0'

class GPS():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0')
        self.north = 0.0
        self.west = 0.0
        self.line = ""

    def getCoords(self):
        found = False
        while(not found):
            self.line = self.ser.readline()
            self.line = list(self.line)
            del self.line[0]
            self.line = bytes(self.line).decode('utf-8')
            if self.line.find('GPGLL') != 1:
                found = True
        N_start = x.find(',') + 1
        N_end = x.find(',', N_start)
        W_start = x.find('N,') + 3
        W_end = x.find(',', W_start)
        self.north = self.line[N_start:N_end]
        self.west = self.line[W_start:W_end]
        return (self.north, self.west)

    def __del__(self):
        del self.ser, self.north, self.west, self.line 

if __name__ == "__main__":
    gps = GPS()
    while (True):
        try:
            coords = gps.getCoords()
            print('N', coords[0], '; W', coords[1])
        except KeyboardInterrupt:
            del gps
            break