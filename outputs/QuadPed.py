# this class serves to drive the motors on a cheap chinese car 
# with directional servo GPIO. Motor and servo layout: 

#           (wheel) MOTOR1 (wheel) 
#             ------servo------
#
#           (wheel) MOTOR2 (wheel)

# Car is all-wheel drive but left an right wheel work in coordination

#class constructor: x = drive(in1, in2, in3, in4) -> BOARD PINS 

from outputs.biMotor import biMotor

class drivetrain:
    #using BCM pins 17, 27, 22, 23
    def __init__(self, m1pos, m1neg,  m2pos, m2neg):
        self.motor1 = biMotor(m1pos, m1neg)
        self.motor2 = biMotor(m2pos, m2neg)
        self.fr = 0 # forward/reverse direction
        self.lr = 0 # left/right direction
    
    def stop(self):
        self.motor1.setSpeed(0)
        self.motor2.setSpeed(0)
        
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
        self.motor1.setSpeed(self.fr)
        self.motor2.setSpeed(self.lr)
    
    # for debugging purposes
    def print(self):
        print("forward/reverse =", self.fr)
        print("left/right =", self.lr)
        
    def __del__(self):
        del self.motor1
        del self.motor2
#end drivetrain class


if __name__ == "__main__":
    import time
    d = drivetrain(17, 27, 22, 23)

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