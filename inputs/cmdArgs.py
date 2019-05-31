import os
import argparse
import configparser
# create an object fill it with default variables from the file 'defaults.ini'
Config = configparser.ConfigParser()
Config.read("./inputs/defaults.ini")

#add description to program's help screen
parser = argparse.ArgumentParser(description='Firmware For a Robot = F^2R. Please try using quotes to encompass values. ie "9;i2c;0x6a,0x1e"')

# add option '--host' for domain name address
parser.add_argument('--host', default=None, help='Type IP address (domain). "0.0.0.0" is for localhost domain.')

# add option '--pipins' for domain name address of pi running pigpiod EXPERIMENTAL!!!
parser.add_argument('--pipins', default=None, help='Type IP address hostname of pi rynning "pigpiod"')

# add option '--port' for domain name address
parser.add_argument('--port', default=None, help='Type port number for the server. "5555" is default.')

# add option '--d' for drivetrain and pin #s
parser.add_argument('--d', default=None, help='Select drivetrain type. "2" = usb+arduino. "1" = bi-ped (R2D2 - like). "0" = quad-Ped (race car setup). Specify the interface in text (ie "gpio", "serial", or "i2c"). Any comma seperated list of numbers delimited by a colon that follow the <type>:<interface>: will be taken as the address of GPIO pins for each motor. ie "1:gpio:18,17:13,22"')

# add option '--m' for motor driver
parser.add_argument('--m', default=None, help='comma seperated list of Motor Driver IC type (with order corresponding to order of appearance in --d address arg). "1" = motor uses 1 PWM + 1 direction signals. "0" = motor uses 2 PWM signals')

# add option '--dof' for Degrees of Freedom and I2C addresses
parser.add_argument('--dof', default=None, help='Select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. Optionally specify the interface in text (ie "serial" or "i2c"). Any additionally comma separated numbers or text that follow the <#DOF>:<interface>: will be used as interface address(es). ie "9:i2c:0x6b,0x1e"')

# add option '--gps' for Degrees of Freedom and I2C addresses
parser.add_argument('--gps', default=None, help='Select type of connection to gps module. Default = "serial", but can also be "i2c" or "spi". Any additionally comma separated items that follow the <interface>: will be used as interface address(es). ie "i2c:0x6a,0x1c" or "serial:comm3". The "spi: flag ignores additional address arguments.')

# add option '--d' for drivetrain and pin #s
parser.add_argument('--cam', default=None, help='Toggle camera. "1" = on (default); "0" = off.')

# thinking of making a '--dev' option to escape the exception hunting
# also options specific to picam and/or opencv2

#use a class to store cmd args 'arg.<option name> = string <value>'
class args:
    def __init__(self):
        # parse arguments using self as storage
        # each parser.add_argument() can be accessed using self.<option flag>
        parser.parse_args(namespace=self)
        # overide defaults with changes
        self.get_whoami()
        self.get_dof()
        self.get_drivetrain()
        self.get_cam()
        self.get_gps()
        self.getPiPins()
        self.get_Phased()

    def getPiPins(self):
        if self.pipins != None:
            from gpiozero.pins.pigpio import PiGPIOFactory
            #set host to hostname or ip address of rPi w/ pigpiod running
            self.pipins = PiGPIOFactory(host=self.pipins)
            
    def get_Phased(self):
        if self.m != None:
            temp = self.m.rsplit(',')
            for i in range(len(temp)):
                temp[i] = str(int(temp[i]))
            Config['Drivetrain']['phasedM'] = ','.join(temp)
    

    # override [] operators to return the Config dictionaries
    def __getitem__(self, key):
        return Config[key]

    def __setitem__(self, key, val):
        Config[key] = str(val)

    # wrap get() function from configparser
    def get(self, section, option):
        return Config.get(section, option)
    
    # wrap getboolean() function from configparser
    def getboolean(self, section, option):
        return Config.getboolean(section, option)

    def get_gps(self):
        # set gps variable
        if self.gps != None:
            temp = self.gps.rsplit(':')
            # print(repr(self.gps))
            Config['GPS']['interface'] = temp[0]
            if len(temp) > 1:
                del temp[0]
                Config['GPS']['address'] = ','.join(temp)
            else: Config['GPS']['address'] = ' '

    def get_cam(self):
        if self.cam != None:
            Config['Camera']['enabled'] = self.cam

    def get_whoami(self):
        # set on_raspi variable
        # if os.name == 'nt':
        self.on_raspi = 'false'
        # print(os.environ)
        if os.name == 'posix':
            # temp = os.system('grep Hardware /proc/cpuinfo')
            import subprocess
            res = subprocess.check_output(["grep", "Hardware", "/proc/cpuinfo"])
            res = res.decode('utf-8')
            for line in res.splitlines():
                if (line.find('BCM') > 1):
                    self.on_raspi = 'true'
                break
        # save onRaspi
        Config['WhoAmI']['onRaspi'] = self.on_raspi
        # save host and port when applicable
        if self.port != None:
            Config['WhoAmI']['port'] = self.port
        if self.host != None:
            Config['WhoAmI']['host'] = self.host

    def get_dof(self):
        # set DoF variable
        if self.dof != None:
            temp = self.dof.rsplit(':')
            # print(repr(temp))
            if len(temp) >= 2:
                Config['IMU']['dof'] = temp[0]
                del temp[0]
                Config['IMU']['interface'] = temp[0]
                del temp[0]
                Config['IMU']['address'] = ','.join(temp)
            else: 
                Config['IMU']['dof'] = temp[0]
                Config['IMU']['address'] = ' '

    def get_drivetrain(self):
        # set drivetrain section
        if self.d != None:
            temp = self.d.rsplit(':')
            # print(repr(temp))
            Config['Drivetrain']['motorConfig'] = temp[0]
            if len(temp) >= 2:
                del temp[0]
                Config['Drivetrain']['interface'] = temp[0]
                del temp[0]
                if len(temp) > 0:
                    Config['Drivetrain']['address'] = ':'.join(temp)
                else: Config['Drivetrain']['address'] = ' '


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
    cmd = args()
    print('Domain:', cmd["WhoAmI"]["host"])
    print('port #:', cmd["WhoAmI"]["port"])
    print('on_raspi:', cmd["WhoAmI"]["onRaspi"])
    print('Degrees of Freedom:', cmd["IMU"]["dof"])
    print('\t',cmd['IMU']['interface'], cmd["IMU"]["address"])
    print('drivetrain type:', cmd['Drivetrain']['motorConfig'])
    print('\t', cmd["Drivetrain"]["interface"], cmd["Drivetrain"]["address"])
    print('motor direction pin:', cmd.getboolean("Drivetrain", "phasedM"))
    print('GPS config:', cmd["GPS"]["interface"], cmd["GPS"]["address"])
    print('camera:', cmd["Camera"]["enabled"])
    print('DistanceSensors:', cmd.get("DistanceSensors", "enabled"))
