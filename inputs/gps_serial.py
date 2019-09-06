"""
GPS_SERIAL
================

Yet another NMEA sentence parser for serial UART based GPS modules. This implements the threaded module for [psuedo] asynchronous applications. CAUTION: The individual satelite info is being ignored until we decide to support capturing it from the GPS module's output.
"""
import serial
import time
import threading

# default location hard-coded to DVC Engineering buildings' courtyard
DEFAULT_LOC = {'lat': 37.96713657090229, 'lng': -122.0712176165581}

def convert2deg(nmea):
    """VERY IMPORTANT needed to go from format 'ddmm.mmmm' into decimal degrees"""
    if nmea is None or len(nmea) < 3:
        return None
    nmea = float(nmea)
    return (nmea // 100) + (nmea - ((nmea // 100) * 100)) / 60

class GPS_SERIAL():
    """
    :param int address: The serial port address that the GPS module is connected to. For example, on the raspberry pi's GPIO pins, this is '/dev/ttyS0'; on windows, this is something like 'com#' where # is designated by windows.
    :param int timeout: Specific number of seconds till the threaded readline() operation expires. Defaults to 1 second.
    """
    def __init__(self, address, timeout=1.0):
        self._dummy = False
        try:
            self._ser = serial.Serial(address, timeout=timeout)
            self.timeOut = timeout
            self._line = self._ser.readline()  # discard any garbage artifacts
            self._gps_thread = None
            print('Successfully opened port', address, 'to GPS module')
        except serial.SerialException:
            self._dummy = True
            print('unable to open serial GPS module @ port', address)
        self.lat = DEFAULT_LOC['lat']
        self.lng = DEFAULT_LOC['lng']
        self.utc = None
        self._line = ""
        self.speed = {"knots": 0.0, "kmph": 0.0}
        self.course = {"true": 0.0, "mag": 0.0}
        self.sat = {"connected": 0, "view": 0, "quality": "Fix Unavailable"}
        self.altitude = 0.0
        # self.azimuth = 0.0
        # self.elevation = 0.0
        self.fix = "no Fix"
        self.rx_status = "unknown"
        self.pdop = 0.0
        self.hdop = 0.0
        self.vdop = 0.0

    def _parse_line(self, str):
        found = False
        if str.find('GLL') != -1:
            found = True
            arr = str.rsplit(',')[1:]
            # print(repr(arr))
            if len(arr[1]) > 1:
                self.lat = convert2deg(arr[0])
                if arr[1] != 'N' and arr[1] is not None:
                    self.lat *= -1
                self.lng = convert2deg(arr[2])
                if arr[3] != 'E' and arr[3] is not None:
                    self.lng *= -1.0
            typeState = {'A': 'data valid', 'V': 'Data not valid'}
            self.data_status = typeState[arr[5]]
        elif str.find('VTG') != -1:
            arr = str.rsplit(',')[1:]
            if len(arr[0]) > 1:
                self.course["true"] = float(arr[0])
            if len(arr[1]) > 1:
                self.course["mag"] = float(arr[1])
            if len(arr[2]) > 1:
                self.speed["knots"] = float(arr[2])
            if len(arr[3]) > 1:
                self.speed["kmph"] = float(arr[3])
        elif str.find('GGA') != -1:
            typeState = [
                "Fix Unavailable", "Valid Fix (SPS)", "Valid Fix (GPS)", "unknown1", "unknown2", "unknown3"]
            arr = str.rsplit(',')[1:]
            self.sat["quality"] = typeState[int(arr[5])]
            self.sat["view"] = int(arr[6])
            if len(arr[8]) > 1:
                self.altitude = float(arr[8])
        elif str.find('GSA') != -1:
            arr = str.rsplit(',')[1:]
            typeFix = ["No Fix", "2D", "3D"]
            self.fix = typeFix[int(arr[1]) - 1]
            self.pdop = float(arr[14])
            self.hdop = float(arr[15])
            self.vdop = float(arr[16][:-3])
        elif str.find('RMC') != -1:
            status = {"V": "Warning", "A": "Valid"}
            arr = str.rsplit(',')[1:]
            self.rx_status = status[arr[1]]
            if len(arr[0]) > 1 and len(arr[8]) > 1:
                self.utc = time.struct_time((2000+int(arr[8][4:6]), int(arr[8][2:4]), int(arr[8][0:2]), int(arr[0][0:2]), int(arr[0][2:4]), int(arr[0][4:6]), 0, 0, -1))
        elif str.find('GSV') != -1:
            arr = str.rsplit(',')[1:]
            self.sat['connected'] = arr[0]
            # ignoring data specific to individual satelites
            # self.elevation = int(arr[4])
            # self.azimuth = int(arr[5])
            # print('sat["view"]:', self.sat["connected"], 'elevation:', self.elevation, 'Azimuth:', self.azimuth)
        return found

    def _threaded_Read(self, raw):
        found = False
        while not found:
            self._line = self._ser.readline()
            try:
                self._line = str(self._line, 'ascii').strip()
            except UnicodeError:
                continue # there was undecernable garbage data that couldn't get encoded to ASCII
            if raw:
                print(self._line)
            # found = true if gps coordinates are captured
            found = self._parse_line(self._line)

    def getData(self, raw=False):
        """
        This function only starts the process of parsing the data from a GPS module (if any).

        :param bool raw: `True` prints the raw data being parsed from the GPS module. `False` doesn't print the raw data. Defaults to `False`.

        :returns: the last latitude and longitude coordinates obtained from either object instantiation (zero values) or previously completed parsing of GPS data.
        """
        if not self._dummy:
            if self._gps_thread != None:
                self._gps_thread.join()
            self._gps_thread = threading.Thread(
                target=self._threaded_Read, args=[raw])
            self._gps_thread.start()
        return {"lat": self.lat, "lng": self.lng}


if __name__ == "__main__":
    # handle cmd line args
    import os
    import argparse
    # add description to program's help screen
    parser = argparse.ArgumentParser(
        description='testing purposes. Please try using quotes to encompass values. ie "COM5" or "/dev/ttyS0"')
    gps_defaults = 'com6'
    parser.add_argument('--p', default=gps_defaults,
                        help='Select serial port address. ie "COM3" or "/dev/ttyS0"')

    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
    cmd = args()
    # finish get cmd line args

    gps = GPS_SERIAL(cmd.p)
    # gps = GPS_SERIAL('/dev/ttyS0')
    while True:
        try:
            gps.getData() # pass `1` or `true` to print raw data from module
            if gps.rx_status.startswith('Valid'):
                print('RxStatus:', gps.rx_status, 'FixType:', gps.fix)
                print('satelites\' quality:', gps.sat["quality"])
                print('satelites connected:', gps.sat["connected"])
                print('satelites in view:', gps.sat['view'])
                print('Course True North:', gps.course["true"], 'degrees')
                print('Course Magnetic North:', gps.course["mag"], 'degrees')
                print('speed in knots:', gps.speed["knots"], 'speed in kmph:', gps.speed["kmph"])
                print('Altitude:', gps.altitude, 'meters')
                print('UTC: {}/{}/{} {}:{}:{}'.format(gps.utc[1], gps.utc[2], gps.utc[0], gps.utc[3], gps.utc[4], gps.utc[5]))
                print('lat:', gps.lat, 'lng:', gps.lng)
                print('position dilution of precision:', gps.pdop, 'meters')
                print('horizontal dilution of precision:', gps.hdop, 'meters')
                print('vertical dilution of precision:', gps.vdop, 'meters\n')
            else:
                print('Waiting for gps fix')
            time.sleep(1)
        except KeyboardInterrupt:
            del gps
            break
