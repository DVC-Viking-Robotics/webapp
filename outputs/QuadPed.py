# this class serves to drive the motors on a cheap chinese car 
# with directional servo GPIO. Motor and servo layout: 

#           (wheel) MOTOR1 (wheel) 
#             ------servo------
#
#           (wheel) MOTOR2 (wheel)

# Car is all-wheel drive but left an right wheel work in coordination

#class constructor: x = drive(in1, in2, in3, in4) -> BOARD PINS 

# from outputs.biMotor import biMotor

class drivetrain:
    #using BCM pins 18, 17, 13, 22
    def __init__(self, m1F, m1B,  m2F, m2B, phased = False):
        if phased:  
            from gpiozero import PhaseEnableMotor as biMotor
            # from outputs.biMotor_bool import biMotor # using High Amperage driver
            self.motor1 = biMotor(m1F, m1B)
            self.motor2 = biMotor(m2F, m2B)
        else: 
            from gpiozero import Motor as biMotor
            # from outputs.biMotor import biMotor # using a L298 or similar driver
            self.motor1 = biMotor(m1F, m1B)
            self.motor2 = biMotor(m2F, m2B)
        self.fr = 0 # forward/reverse direction
        self.lr = 0 # left/right direction
    
    def stop(self):
        # from old biMotor class
        # self.motor1.setSpeed(0)
        # self.motor2.setSpeed(0)
        self.motor1.stop()
        self.motor2.stop()
        
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