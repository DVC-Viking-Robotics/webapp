class Drivetrain(object):
    #using BCM pins 18, 17, 13, 22
    def __init__(self, m1F, m1B,  m2F, m2B, phased = False):
        if phased:  
            from gpiozero import PhaseEnableMotor as biMotor
            # from outputs.biMotor_bool import biMotor # using High Amperage driver
        else: 
            from gpiozero import Motor as biMotor
            # from outputs.biMotor import biMotor # using a L298 or similar driver
        self.motor1 = biMotor(m1F, m1B)
        self.motor2 = biMotor(m2F, m2B)

    
    def stop(self):
        # from old biMotor class
        # self.motor1.setSpeed(0)
        # self.motor2.setSpeed(0)
        self.motor1.stop()
        self.motor2.stop()
        
    def __del__(self):
        del self.motor1
        del self.motor2
#end Drivetrain class

class BiPed(Drivetrain):
    #using BCM pins 18, 17, 13, 22
    def __init__(self, m1F, m1B,  m2F, m2B, phased = False):
        super(BiPed, self).__init__(m1F, m1B,  m2F, m2B, phased)
        self.right = 0
        self.left = 0

    # pass backwards/forward (-100 to 100) as variable x
    # pass left/right (-100 to 100) as variable y
    def go(self, x, y):
        # make sure arguments are in their proper range
        x = max(-100, min(100, x))
        y = max(-100, min(100, y))
        # assuming left/right axis is null (just going forward or backward)
        self.left = y
        self.right = y
        if y == 0: 
            # if forward/backward axis is null ("turning on a dime" functionality)
            self.right = -1 * x
            self.left = x
        else: 
            # if forward/backward axis is not null and left/right axis is not null
            if x > 0:
                self.right = y * ((100 - x) / 100.0)
            elif x < 0:
                self.left = y * ((-100 - x) / 100.0) * -1
        # make sure speeds are an integer (not decimal/float) and send to motors
        # from old biMotor class(s)
        # self.motor1.setSpeed(int(round(self.right)))
        # self.motor2.setSpeed(int(round(self.left)))
        if self.right > 0:
            self.motor1.backward(self.right/ 100.0)
        elif self.right < 0:
            self.motor1.forward(self.right * -0.01)
        else:
            self.motor1.stop()
        
        if self.left > 0:
            self.motor2.backward(self.left / 100.0)
        elif self.left < 0:
            self.motor2.forward(self.left * -0.01)
        else:
            self.motor2.stop()
        
    # for debugging purposes
    def print(self):
        print("left =", self.left)
        print("right =", self.right)
#end BiPed class

class QuadPed(Drivetrain):
    #using BCM pins 18, 17, 13, 22
    def __init__(self, m1F, m1B,  m2F, m2B, phased = False):
        super(QuadPed, self).__init__(m1F, m1B, m2F, m2B, phased)
        self.fr = 0 # forward/reverse direction
        self.lr = 0 # left/right direction

    # pass backwards/forward (-100 to 100) as variable x
    # pass left/right (-100 to 100) as variable y
    def go(self, x, y):
        # make sure arguments are in their proper range
        # make sure speeds are an integer (not decimal/float)
        x = int(round(max(-100, min(100, x))))
        y = int(round(max(-100, min(100, y))))
        # set the axis directly to their corresponding motors
        self.fr = y
        self.lr = x
        
        # from old biMotor class
        # self.motor1.setSpeed(self.fr)
        # self.motor2.setSpeed(self.lr)
        
        if self.fr > 0:
            self.motor1.forward(self.fr / 100.0)
        elif self.fr < 0:
            self.motor1.backward(self.fr * -0.01)
        else:
            self.motor1.stop()

        if self.lr > 0:
            self.motor2.forward(self.lr / 100.0)
        elif self.lr < 0:
            self.motor2.backward(self.lr * -0.01)
        else:
            self.motor2.stop()
    
    # for debugging purposes
    def print(self):
        print("forward/reverse =", self.fr)
        print("left/right =", self.lr)
#end QuadPed class




if __name__ == "__main__":
    import time
        #handle cmd line args
    import os
    import argparse
    #add description to program's help screen
    parser = argparse.ArgumentParser(description='testing purposes. Please try using quotes to encompass values. ie "0" or "1"')
    gps_defaults = '0'
    parser.add_argument('--d', default=gps_defaults, help='Select drivetrain type. "1" = bi-ped (R2D2 - like); "0" = quad-Ped (race car setup).')
    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
            self.d = int(self.d)
    cmd = args()
    #finish get cmd line args
    
    if(cmd.d == 1):
        d = BiPed(17, 27, 22, 23)
    else: d = QuadPed(17, 27, 22, 23)
    d.go(100, 0)
    time.sleep(2)
    d.go(0, 100)
    time.sleep(2)
    d.go(100, 100)
    time.sleep(2)
    d.go(-100, 0)
    time.sleep(2)
    d.go(0, -100)
    time.sleep(2)
    d.go(-100, -100)
    time.sleep(2)
    d.stop()

    del d