import os
import argparse
#add description to program's help screen
parser = argparse.ArgumentParser(description='Firmware For a Robot = F^2R')

# default variables used to do stuff
biPed = True
phasedM = True
DoF = '6' # degree of freedom and i2cdetect address(s)
# use '9,0x6a,0x1c' for LSM9DS1
# use '6,0x68' foy GY-521
on_raspi = True

# add option '--d' for drivetrain
parser.add_argument('--d', choices=['1', '0'], default=int(biPed), help='select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup)')

# add option '--m' for motor driver
parser.add_argument('--m', choices=['1', '0'], default=int(phasedM), help='select Motor Driver IC type. "1" = PWM + direction signals per motor. "0" = 2 PWM signals per motor')

# add option '--dof' for Degrees of Freedom and I2C addresses
parser.add_argument('--dof', default=DoF, help='select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. any additionally comma separated numbers that follow will be used as i2c addresses. ie "9,0x6a,0x1c"')

# thinking of making a '--dev' option to escape the exception hunting
# also options specific to picam and/or opencv2

#use a class to store cmd args 'arg.<option name> = string <value>'
class args:
    def __init__(self):
        parser.parse_args(namespace=self)
        self.biPed = bool(int(self.d))
        self.phasedM = bool(int(self.m))
        self.DoF = []
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
        temp = self.dof.rsplit(',')
        if (len(temp) > 1):
            # print(repr(temp))
            for i in range(len(temp)):
                num = int(temp[i], 16)
                if not i:
                    num = int(temp[i])
                elif num < 0x03 or num > 0x77:
                    print(num, 'is not a valid i2c address')
                    break
                self.DoF.append(num)
        else:
            self.DoF = [int(self.dof[0])]

if __name__ == "__main__":
    # instatiate this object to invoke the __init__() that translates the strings to usable data
    std = args()
    print('on_raspi:', std.on_raspi)
    print('DoF:', repr(std.DoF))
    print('biPed:', std.biPed)
    print('motor direction pin:', std.phasedM)