import os
import argparse
#add description to program's help screen
parser = argparse.ArgumentParser(description='Firmware For a Robot = F^2R. Please try using quotes to encompass values. ie "9,0x6a,0x1e"')

# default variables used to do stuff
biPed = '1,18,17,13,22'
phasedM = '1'
DoF = '6' # degree of freedom and i2cdetect address(s)
# use '9,0x6a,0x1c' for LSM9DS1
# use '6,0x68' foy GY-521
on_raspi = True
gps_defaults = 'serial,/dev/ttyS0'

# add option '--d' for drivetrain and pin #s
parser.add_argument('--d', default=biPed, help='select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup). Any numbers that follow will be taken as pairs for the GPIO pins to each motor. 1,18,17,13,22 is the default.')

# add option '--m' for motor driver
parser.add_argument('--m', choices=['1', '0'], default=int(phasedM), help='select Motor Driver IC type. "1" = PWM + direction signals per motor. "0" = 2 PWM signals per motor')

# add option '--dof' for Degrees of Freedom and I2C addresses
parser.add_argument('--dof', default=DoF, help='select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. any additionally comma separated numbers that follow will be used as i2c addresses. ie "9,0x6a,0x1c"')

# add option '--gps' for Degrees of Freedom and I2C addresses
parser.add_argument('--gps', default=gps_defaults, help='select type of cennection to gps module. Default = "serial", but can also be "i2c" or "spi". Any additionally comma separated items that follow will be used as i2c addresses or serial address. ie "i2c,0x6a,0x1c" or "serial,comm3". The "spi: flag ignores additional arguments.')

# thinking of making a '--dev' option to escape the exception hunting
# also options specific to picam and/or opencv2

#use a class to store cmd args 'arg.<option name> = string <value>'
class args:
    def __init__(self):
        # parse arguments using self as storage
        # each parser.add_argument() can be accessed using self.<option flag>
        parser.parse_args(namespace=self)
        self.biPed = []
        self.phasedM = 0
        self.DoF = []
        self.gps_conf = []
        self.get_onRaspi()
        self.get_dof()
        self.get_biPed()
        self.getPhased()
        self.get_gps()

    def get_gps(self):
        #set gps variable
        self.gps_conf = self.gps.rsplit(',')
        # print(repr(self.gps))
        if len(self.gps_conf) > 1:
            for i in range(1,len(self.gps_conf)):
                if self.gps_conf[0] == 'serial':
                    pass
                if self.gps_conf[0] == 'spi':
                    self.gps_conf.pop()
                if self.gps_conf[0] == 'i2c' and self.is_valid_i2c(int(self.gps_conf[i], 16)):
                    self.gps_conf[i] = num
        temp = gps_defaults.rsplit(',')
        while len(self.gps_conf) < len(temp):
            self.gps_conf.append(temp[len(self.gps_conf)])


    def getPhased(self):
        self.phasedM = bool(int(self.m))

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
            elif not self.is_valid_i2c(num):
                break
            self.DoF.append(num)

    def is_valid_BCM(self, n):
        if n < 0 or n > 27:
            print(n, 'is not a valid BCM pin #')
            return False
        else: return True

    def get_biPed(self):
        #set biPed variable
        temp = self.d.rsplit(',')
        # print(repr(temp))
        for i in range(len(temp)):
            num = int(temp[i])
            if not self.is_valid_BCM(num):
                break
            self.biPed.append(num)
        temp = biPed.rsplit(',')
        while len(self.biPed) < len(temp):
            self.biPed.append(int(temp[len(self.biPed)]))

    def is_valid_i2c(self, n):
        if n < 0x03 or n > 0x77:
            print(n, 'is not a valid i2c address')
            return False
        else: return True



if __name__ == "__main__":
    # instatiate this object to invoke the __init__() that translates the strings to usable data
    std = args()
    print('on_raspi:', std.on_raspi)
    print('DoF:', repr(std.DoF))
    print('biPed:', std.biPed)
    print('motor direction pin:', std.phasedM)
    print('GPS config:', repr(std.gps_conf))
