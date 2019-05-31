from gpiozero import AngularServo, PhaseEnableMotor, Motor, PinPWMUnsupported
try:
    from outputs.stepperMotor import Stepper
except ImportError:# for self exec loop
    from stepperMotor import Stepper

class dummyMotor:
    def __init__(self, value = 0):
        self.value = value

class Drivetrain(object):
    # using BCM pins = [[18,17], [13,22], [4], [5,6,12,16]]
    # phased = "true,false" order correspnding to order of DC motor pins that are passed
    def __init__(self, pins, phased, maxSpeed, pin_factory):
        self.motors = []
        self.maxSpeed = max(0, min(maxSpeed, 100)) # ensure proper range
        phased = phased.rsplit(',')
        for phased_i in range(len(phased)):
            phased[phased_i] = bool(int(phased[phased_i]))
        phased_i = 0
        for i in range(len(pins)):
            try:
                if len(pins[i]) == 1: # use servo
                    print('motor', i, 'Servo @', repr(pins[i]))
                    self.motors.append(AngularServo(pins[i][0], pin_factory = pin_factory))
                elif len(pins[i]) == 4: # use bipolar stepper
                    print('motor', i, 'Stepper @', repr(pins[i]))
                    self.motors.append(Stepper([pins[i][0], pins[i][1],pins[i][2], pins[i][3]], pin_factory = pin_factory))
                elif len(pins[i]) == 2: # use DC bi-directional motor
                    print('motor', i, 'DC @', repr(pins[i]), 'phased:', phased[phased_i])
                    if phased_i < len(phased) and phased[phased_i]: 
                        # is the flag specified and does it use a Phase control signal 
                        self.motors.append(PhaseEnableMotor(pins[i][0], pins[i][1], pin_factory = pin_factory))
                    else: 
                        self.motors.append(Motor(pins[i][0], pins[i][1], pin_factory = pin_factory))
                    phased_i += 1
                else:
                    print('unknown motor type from', len(pins[i]), '=', repr(pins[i]))
            except PinPWMUnsupported: # except on PC during DEV mode 
                self.motors.append(dummyMotor())

    def gogo(self, zAux):
        if len(zAux) > 2:
            for i in range(2, len(zAux)):
                if i < len(self.motors):
                    print('motor[', i, '].value = ', zAux[i] / 100.0, sep = '')
                    self.motors[i].value = zAux[i] / 100.0
                else: print('motor[', i, '] not declared and/or installed', sep = '')
  
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
    def __init__(self, pins, phased = 'True,False', maxSpeed = 85, pin_factory = None):
        super(BiPed, self).__init__(pins, phased, maxSpeed, pin_factory = pin_factory)
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
        self.motors[0].value = self.left / 100.0
        self.motors[1].value = self.right / 100.0
        self.gogo(cmds)
    
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
    def __init__(self, pins, phased = 'False,False', maxSpeed = 85, pin_factory = None):
        super(QuadPed, self).__init__(pins, phased, maxSpeed, pin_factory = pin_factory)
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
        if type(self.motors[0]) is dummyMotor:
            print("left =", self.lr)
        else:
            self.motors[0].value = self.lr / 100.0
        if type(self.motors[1]) is dummyMotor:
            print("right =", self.fr)
        else:
            self.motors[1].value = self.fr / 100.0
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
    d_defaults = '1'
    m_defaults = 'false,false'
    parser.add_argument('--d', default=d_defaults, help='Select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup).')
    parser.add_argument('--m', default=m_defaults, help='list of dc motor phase flags. "true" = 1 PWM + 1 Dir pins per motor; "false" = 2 PWM pins per motor.')
    parser.add_argument('--pipins', default=None, help='list of dc motor phase flags. "true" = 1 PWM + 1 Dir pins per motor; "false" = 2 PWM pins per motor.')
    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
            self.d = int(self.d)
            # use mock pin factory
            from gpiozero.pins.mock import MockFactory
            from gpiozero.pins.pigpio import PiGPIOFactory
            if self.pipins != None: self.pipins = PiGPIOFactory(host=self.pipins)
            else: self.pipins = MockFactory()
    cmd = args()
    # finish get cmd line args
    if(cmd.d == 1):
        myPins = [[18,17], [13,22]]
        # , [5,6,12,16]
        d = BiPed(myPins, cmd.m, pin_factory = cmd.pipins)
    else: 
        myPins = [[18,17], [13, 22]]
        # , [4]
        d = QuadPed(myPins, cmd.m, pin_factory = cmd.pipins)
    d.go([100, 0, 50])
    time.sleep(2)
    d.go([0, 100, -25])
    time.sleep(2)
    d.go([100, 100, 0])
    time.sleep(2)
    d.go([-100, 0])
    time.sleep(2)
    d.go([0, -100])
    time.sleep(2)
    d.go([-100, -100, 50])
    time.sleep(2)
    d.go([0, 0, 0])

    del d