import os
import argparse
#add description to program's help screen
parser = argparse.ArgumentParser(description='Firmware For a Robot = F^2R. Please try using quotes to encompass values. ie "9,0x6a,0x1e"')

# default variables used to do stuff
driveT = '1,18,17,13,22'
phasedM = '1'
DoF = '6' # degree of freedom and i2cdetect address(s)
# use '9,0x6a,0x1c' for LSM9DS1
# use '6,0x68' foy GY-521
on_raspi = True
gps_defaults = 'serial,/dev/ttyS0'
cam_default = '1'
host = '0.0.0.0'
port = '5555'

# add option '--host' for domain name address
parser.add_argument('--host', default=host, help='Type IP address (domain). "0.0.0.0" is for localhost domain.')

# add option '--port' for domain name address
parser.add_argument('--port', default=port, help='Type port number for the server. "5555" is default.')

# add option '--d' for drivetrain and pin #s
parser.add_argument('--d', default=driveT, help='Select drivetrain type. "2" = usb+arduino. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup). Any numbers that follow will be taken as pairs for the GPIO pins to each motor. ie "1,18,17,13,22".')

# add option '--m' for motor driver
parser.add_argument('--m', choices=['1', '0'], default=int(phasedM), help='Select Motor Driver IC type. "1" = PWM + direction signals per motor. "0" = 2 PWM signals per motor')

# add option '--dof' for Degrees of Freedom and I2C addresses
parser.add_argument('--dof', default=DoF, help='Select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. Any additionally comma separated hexadecimal numbers that follow will be used as i2c addresses. ie "9,0x6a,0x1c"')

# add option '--gps' for Degrees of Freedom and I2C addresses
parser.add_argument('--gps', default=gps_defaults, help='Select type of connection to gps module. Default = "serial", but can also be "i2c" or "spi". Any additionally comma separated items that follow will be used as i2c addresses or serial address. ie "i2c,0x6a,0x1c" or "serial,comm3". The "spi: flag ignores additional arguments.')

# add option '--d' for drivetrain and pin #s
parser.add_argument('--cam', default=cam_default, choices=['1', '0'], help='Toggle camera. "1" = on (default); "0" = off.')

# thinking of making a '--dev' option to escape the exception hunting
# also options specific to picam and/or opencv2

#use a class to store cmd args 'arg.<option name> = string <value>'
class args:
    def __init__(self):
        # parse arguments using self as storage
        # each parser.add_argument() can be accessed using self.<option flag>
        parser.parse_args(namespace=self)
        self.driveT = []
        self.phasedM = 0
        self.DoF = []
        self.gps_conf = []
        
        # parse algo
        self.get_onRaspi()
        self.get_dof()
        self.get_driveT()
        self.get_Phased()
        self.get_cam()
        self.get_gps()
        self.get_port()

    def get_port(self):
        self.port = int(self.port)

    def get_gps(self):
        #set gps variable
        self.gps_conf = self.gps.rsplit(',')
        # print(repr(self.gps))
        if len(self.gps_conf) > 1:
            i = 1
            while i < len(self.gps_conf):
                if bool(i):
                    if self.gps_conf[0] == 'spi':
                        self.gps_conf.pop()
                    if self.gps_conf[0] == 'i2c':
                        num = int(self.gps_conf[i], 16)
                        if self.is_valid_i2c(num):
                            self.gps_conf[i] = num
                        else: 
                            self.gps_conf.pop(i)
                            i = i - 1
                i = i + 1
        if self.gps_conf[0] == 'serial':
            # auto fill in defaults
            temp = gps_defaults.rsplit(',')
            while len(self.gps_conf) < len(temp):
                self.gps_conf.append(temp[len(self.gps_conf)])

    def get_Phased(self):
        self.phasedM = bool(int(self.m))
 
    def get_cam(self):
        self.cam = bool(int(self.cam))

    def get_onRaspi(self):
        #set on_raspi variable
        if os.name == 'nt':
            self.on_raspi = False
            # print(os.environ)
        elif os.name == 'posix':
            # temp = os.system('grep Hardware /proc/cpuinfo')
            import subprocess
            res = subprocess.check_output(["grep", "Hardware", "/proc/cpuinfo"])
            res = res.decode('utf-8')
            for line in res.splitlines():
                if (line.find('BCM') > 1):
                    self.on_raspi = True
                else:
                    self.on_raspi = False
                break

    def get_dof(self):
        #set DoF variable
        temp = self.dof.rsplit(',')
        # print(repr(temp))
        for i in range(len(temp)):
            num = int(temp[i], 16)
            if not i:
                num = int(temp[i])
                self.DoF.append(num)
            elif not self.is_valid_i2c(num):
                pass
            else: self.DoF.append(num)

    def get_driveT(self):
        #set driveT variable
        temp = self.d.rsplit(',')
        # print(repr(temp))
        for i in range(len(temp)):
            num = int(temp[i])
            if not i and not self.is_valid_BCM(num):
                pass
            else: self.driveT.append(num)
        temp = driveT.rsplit(',')
        # fill in rest of the args with the defaults
        while len(self.driveT) < len(temp):
            self.driveT.append(int(temp[len(self.driveT)]))

    def is_valid_BCM(self, n):
        if n < 0 or n > 27:
            print(n, 'is not a valid BCM pin #')
            return False
        else: return True

    def is_valid_i2c(self, n):
        if n < 0x03 or n > 0x77:
            print(n, 'is not a valid i2c address')
            return False
        else: return True



if __name__ == "__main__":
    # instatiate this object to invoke the __init__() that translates the strings to usable data
    std = args()
    print('Domain:', std.host)
    print('port #:', std.port)
    print('on_raspi:', std.on_raspi)
    print('Degrees of Freedom:', repr(std.DoF))
    print('drivetrain:', std.driveT)
    print('motor direction pin:', std.phasedM)
    print('GPS config:', repr(std.gps_conf))
    print('camera:',std.cam)
