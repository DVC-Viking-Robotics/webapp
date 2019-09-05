import serial
import time
import threading

DEFAULT_LOC = {'lat': 37.96713657090229, 'lng': -122.0712176165581}

class GPSserial():
    '''
    GPS serial Output conforms to NMEA format
    addy port address
    t = seconds till timeout
    See the datasheet in this repo
    '''
    def __init__(self, addy, t = 1):
        # open a "channel" (technically I think its called a "handle") to Serial port
        # on rasbian the Tx/Rx pins register as '/dev/ttyS0'
        # on Windows my arduino (connected to GPS6MV2) registers as "COM3"
        # addy passed from inputs/cmdArgs.py
        self.dummy = False
        try:
            self.ser = serial.Serial(addy)
            self.timeOut = t
            self.line = self.ser.readline() # discard any garbage artifacts
            self.GPS_thread = None
            print('Successfully opened port', addy,'to GPS module')
        except serial.SerialException:
            self.dummy = True
            print('unable to open serial GPS module @ port', addy)
        self.NS = DEFAULT_LOC['lat']
        self.EW = DEFAULT_LOC['lng']
        self.UTC = ""
        self.line = ""
        self.speed = {"knots": 0.0, "kmph": 0.0}
        self.course = {"true": 0.0, "mag": 0.0}
        self.sat = {"connected": 0, "view": 0, "quality": "Fix Unavailable"}
        self.alt = 0.0
        self.azi = 0.0
        self.elev = 0.0
        self.fix = "no Fix"
        self.rx_status = "unknown"

    def getCoords(self):
        pass

    def getTime(self):
        if (self.UTC == ""):
            return "no UTC"
        else:
            hr = int(self.UTC[0:2])
            min = int(self.UTC[3:4])
            sec = float(self.UTC[5:])
            return self.UTC

    def parseline(self, str):
        found = False
        if str.find('GLL') != -1:
            arr = str.rsplit(',')
            # print(repr(arr))
            if (len(arr[1]) > 1):
                self.NS = float(arr[1])
                self.NS_dir = arr[2]
                self.EW = float(arr[3])
                self.EW_dir = arr[4]
                if (self.NS_dir != 'N'):
                    self.NS_dir = -1.0
                else:
                    self.NS_dir = 1.0
                if (self.EW_dir != 'E'):
                    self.EW_dir = -1.0
                else:
                    self.EW_dir = 1.0
                found = True
                self.convertGPS()
            if (len(arr[5]) > 1):
                self.UTC = arr[5]
            typeState = {'A': 'data valid', 'V': 'Data not valid'}
            self.data_status = typeState[arr[6]]
        elif (str.find('VTG') != -1):
            arr = str.rsplit(',')
            # print(repr(arr))
            if (len(arr[1]) > 1):
                self.course["true"] = float(arr[1])
            if (len(arr[2]) > 1):
                self.course["mag"] = float(arr[2])
            if (len(arr[3]) > 1):
                self.speed["knots"] = float(arr[3])
            if (len(arr[4]) > 1):
                self.speed["kmph"] = float(arr[4])
        elif (str.find('GGA') != -1):
            typeState = ["Fix Unavailable", "Valid Fix (SPS)", "Valid Fix (GPS)", "unknown1", "unknown2", "unknown3"]
            arr = str.rsplit(',')
            # print(repr(arr))
            self.sat["quality"] = typeState[int(arr[6])]
            self.sat["connected"] = int(arr[7])
            if (len(arr[9]) > 1):
                self.alt = float(arr[9])
        elif (str.find('GSA') != -1):
            typeFix = ["No Fix","2D", "3D"]
            arr = str.rsplit(',')
            # print(repr(arr))
            # print('typeFix:', int(arr[2]))
            self.fix =typeFix[int(arr[2]) - 1]
        elif (str.find('RMC') != -1):
            status = {"V":"Warning","A": "Valid"}
            arr = str.rsplit(',')
            # print(repr(arr))
            self.rx_status = status[arr[2]]
        '''elif (str.find('GSV') != -1):
            arr = str.rsplit(',')
            print(repr(arr))
            self.sat["view"] = int(arr[3])
            self.elev = int(arr[5])
            self.azi = int(arr[6])
            print('sat["view"]:', self.sat["view"], 'elevation:', self.elev, 'Azimuth:', self.azi)
            '''
        return found

    '''VERY IMPORTANT'''
    # needed to go from format 'DDHH.SS' into decimal degrees
    def convertGPS(self):
        lat_DD = int(self.NS/100)
        lat_SS = self.NS - (lat_DD*100)
        latDec = lat_DD + lat_SS/60

        lng_DD = int(self.EW/100)
        lng_SS = self.EW - (lng_DD*100)
        lngDec = lng_DD + lng_SS/60
        self.NS = latDec * self.NS_dir
        self.EW = lngDec * self.EW_dir

    def threaded_Read(self, raw):
        found = False
        while(not found):
            self.line = self.ser.readline()
            if (raw):
                print(self.line)
            self.line = list(self.line)
            del self.line[0]
            self.line = bytes(self.line).decode('utf-8')
            # found = true if gps coordinates are captured
            found = self.parseline(self.line)

    def getData(self, raw = False):
        if not self.dummy:
            if self.GPS_thread != None:
                self.GPS_thread.join()
            self.GPS_thread = threading.Thread(target=self.threaded_Read, args=[raw])
            self.GPS_thread.start()
        return {"lat": self.NS, "lng": self.EW}

if __name__ == "__main__":
    #handle cmd line args
    import os
    import argparse
    #add description to program's help screen
    parser = argparse.ArgumentParser(description='testing purposes. Please try using quotes to encompass values. ie "COM5" or "/dev/ttyS0"')
    gps_defaults = 'com6'
    parser.add_argument('--p', default=gps_defaults, help='Select serial port address. ie "COM3" or "/dev/ttyS0"')
    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
    cmd = args()
    #finish get cmd line args

    gps = GPSserial(cmd.p)
    # gps = GPSserial('/dev/ttyS0')
    while (True):
        try:
            gps.getData()
            print('RxStatus:', gps.rx_status)
            print('FixType:', gps.fix)
            print('sat["quality"]:', gps.sat["quality"], 'sat["connected"]:', gps.sat["connected"], 'Altitude:', gps.alt)
            print('Course True North:', gps.course["true"], 'Course Magnetic North:', gps.course["mag"], 'speed["knots"]:', gps.speed["knots"], 'speed["kmph"]:', gps.speed["kmph"])
            print('UTC:', gps.getTime(), 'NS:',  gps.NS, 'EW:', gps.EW)
            time.sleep(1)
        except KeyboardInterrupt:
            del gps
            break
