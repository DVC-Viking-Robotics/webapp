import os
import argparse
parser = argparse.ArgumentParser(description='Firmware For a Robot = F^2R')
parser.add_argument('--d', choices=['1', '0'], default=1, help='select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup)')
parser.add_argument('--m', choices=['1', '0'], default=1, help='select Motor Driver IC type. "1" = PWM + direction signals per motor. "0" = 2 PWM signals per motor')
parser.add_argument('--dof', default=[9], help='select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. any additionally comma separated numbers that follow will be used as i2c addresses. ie "9,0x6a,0x1c"')

biPed = True
phasedM = True
DoF = [6] # degree of freedom and i2cdetect address(s) as a tuple
# use [9,0x6a,0x1c] for LSM9DS1
# use [6,0x68] foy GY-521
on_raspi = True
# Hardware        : BCM2835
# 0

class args:
    def __init__(self):
        parser.parse_args(namespace=self)
        self.biPed = bool(int(self.d))
        self.phasedM = bool(int(self.m))
        if os.name == 'nt':
            self.on_raspi = False
            # print(os.environ)
        elif os.name == 'posix':
            # temp = os.system('grep Hardware /proc/cpuinfo')
            import subprocess
            res = subprocess.check_output(["grep", "Hardware", "/proc/cpuinfo"])
            print('type=', type(res))
            res = res.decode('utf-8')
            for line in res.splitlines():
                if (line.find('BCM') > 1):
                    self.on_raspi = True
                else:
                    self.on_raspi = False
                break
        if (len(self.dof) > 1):
            temp = self.dof.rsplit(',')
            # print(repr(temp))
            for i in range(1,len(temp)):
                self.DoF.append(int(temp[i]))
        else:
            self.DoF = [int(self.dof[0])]


if __name__ == "__main__":
    std = args()
    print('on_raspi:', std.on_raspi,'DoF:', repr(std.DoF), 'biPed:', std.biPed, 'motor direction pin:', std.phasedM)