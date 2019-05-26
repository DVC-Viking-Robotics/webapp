from gpiozero import AngularServo, PhaseEnableMotor, Motor
from stepperMotor import Stepper
# from outputs.stepperMotor import Stepper
        


class Drivetrain(object):
    motors = []
    # using BCM pins[DCmotors] = [(18, 17), (13, 22)]
    # phased = "true,false" order correspnding to order of DC motor pins that are passed
    def __init__(self, pins, phased, maxSpeed):
        self.maxSpeed = min(maxSpeed, 100) # ensure proper range
        phased_i = 0
        phased = phased.rsplit(',')
        for b in phased:
            b = bool(b)
        for i in range(len(pins)):
            if len(pins[i]) == 1: # use servo
                self.motors.append(AngularServo(pins[i][0]))
            elif len(pins[i]) == 4: # use bipolar stepper
                self.motors.append(Stepper([pins[i][0], pins[i][1],pins[i][2], pins[i][3]]))
            elif len(pins[i]) == 2:
                if phased[phased_i]:  
                    # from outputs.phasedMotor import phasedMotor as PhaseEnableMotor
                    self.motors.append(PhaseEnableMotor(pins[i][0], pins[i][1]))
                else: 
                    # from outputs.biMotor import biMotor as Motor
                    self.motors.append(Motor(pins[i][0], pins[i][1]))
                phased_i += 1

    def gogo(self, zAux):
        for i in range(2, len(zAux)):
            self.motors[i].value = zAux[i] / 100.0
  
    def __del__(self):
        while len(self.motors) > 0:
            del self.motors[len(self.motors) - 1]
        # del self.motors
# end Drivetrain class

class BiPed(Drivetrain):
    """ 
    using BCM pins = [(18,17), (13,22), (4), (5,6,12,16)]
    pins arg contains tuples of pins. 1 tuple per motor. 
      2 pin tuple = bi-directional dc motor
      1 pin tuple = servo motor
      4 pin tuple = stepper motor
      NOTE:the 1st 2 tuples are used to propell and steer respectively
    """
    def __init__(self, pins, phased = True, maxSpeed = 85):
        super(BiPed, self).__init__(pins, phased, maxSpeed)
        self.right = 0
        self.left = 0
    """ 
    pass cmds as [] = [x,y,z,aux,ect]
        pass backwards/forward in range [-100,100] as variable x
        pass left/right in range [-100,100] as variable y
        pass attitude/yaw/roll (as percent angle) in range [-100,100] as variable z, aux, etc
    """
    def go(self, cmds):
        # make sure arguments are in their proper range
        cmds[0] = round(max(-100, min(100, cmds[0])))
        cmds[1] = round(max(-100, min(100, cmds[1])) * (self.maxSpeed / 100.0))
        # assuming left/right axis is null (just going forward or backward)
        self.left = cmds[1]
        self.right = cmds[1]
        if abs(cmds[0]) == 100:
            # if forward/backward axis is null ("turning on a dime" functionality)
            cmds[0] *= self.maxSpeed / 100.0
            self.right = cmds[0]
            self.left = cmds[0] * -1
        else: 
            # if forward/backward axis is not null and left/right axis is not null
            offset = (100 - abs(cmds[0])) / 100.0
            if cmds[0] > 0:
                self.right *= offset
            elif cmds[0] < 0:
                self.left *= offset
        """ for debugging """
        # self.print()
        
        # make sure speeds are an integer (not decimal/float) and send to motors
        if self.right > 0:
            self.motors[0].value = self.right / 100.0
            #self.motors[0].forward(self.right / 100.0)
        elif self.right < 0:
            self.motors[0].value = self.right / -100.0
        else:
            self.motors[0].value = 0
        
        if self.left > 0:
           self.motors[1].value = self.left / 100.0
        elif self.left < 0:
            self.motors[1].value = self.left / -100.0
        else:
            self.motors[1].value = 0
        self.gogo(cmds)

    # for debugging purposes
    def print(self):
        print("left =", self.left)
        print("right =", self.right)
# end BiPed class

class QuadPed(Drivetrain):
    """ 
    using BCM pins = [(18,17), (13,22), (4), (5,6,12,16)]
    pins arg contains tuples of pins. 1 tuple per motor. 
      2 pin tuple = bi-directional dc motor
      1 pin tuple = servo motor
      4 pin tuple = stepper motor
      NOTE:the 1st 2 tuples are used to propell and steer respectively
    """
    def __init__(self, pins, phased = False, maxSpeed = 85):
        super(QuadPed, self).__init__(pins, phased, maxSpeed)
        self.fr = 0 # forward/reverse direction
        self.lr = 0 # left/right direction

    # pass backwards/forward (-100 to 100) as variable x
    # pass left/right (-100 to 100) as variable y
    def go(self, cmds):
        # make sure arguments are in their proper range
        # make sure speeds are an integer (not decimal/float)
        cmds[0] = round(max(-100, min(100, cmds[0])))
        cmds[1] = round(max(-100, min(100, cmds[1])) * (self.maxSpeed / 100.0))
        # set the axis directly to their corresponding motors
        self.fr = cmds[0]
        self.lr = cmds[0]
        if self.lr > 0:
            self.motors[0].value = self.lr / 100.0
        elif self.lr < 0:
            self.motors[0].value = self.lr * -0.01
        else:
            self.motors[0].value = 0
        
        if self.fr > 0:
            self.motors[1].value = self.fr / 100.0
        elif self.fr < 0:
            self.motors[1].value = self.fr * -0.01
        else:
            self.motors[1].value = 0
        self.gogo(cmds)

    # for debugging purposes
    def print(self):
        print("forward/reverse =", self.fr)
        print("left/right =", self.lr)
# end QuadPed class




if __name__ == "__main__":
    import time
    # handle cmd line args
    import os
    import argparse
    # add description to program's help screen
    parser = argparse.ArgumentParser(description='testing purposes. Please try using quotes to encompass values. ie "0" or "1"')
    d_defaults = '0'
    m_defaults = 'false,false'
    parser.add_argument('--d', default=d_defaults, help='Select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup).')
    parser.add_argument('--m', default=m_defaults, help='list of dc motor phase flags. "true" = 1 PWM + 1 Dir pins per motor; "false" = 2 PWM pins per motor.')
    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
            self.d = int(self.d)
    cmd = args()
    # finish get cmd line args
    if(cmd.d == 1):
        myPins = [[18,17], [13,22], [5,6,12,16]]
        d = BiPed(myPins, cmd.m)
    else: 
        myPins = [[18,17], [4], [13]]
        d = QuadPed(myPins, cmd.m)
    d.go([100, 0, 50])
    time.sleep(2)
    d.go([0, 100, 0])
    time.sleep(2)
    d.go([100, 100, -50])
    time.sleep(2)
    d.go([-100, 0, 0])
    time.sleep(2)
    d.go([0, -100, 25])
    time.sleep(2)
    d.go([-100, -100, -25])
    time.sleep(2)
    d.go([0, 0, 0])

    del d