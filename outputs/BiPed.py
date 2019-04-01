class drivetrain():
    #using BCM pins 18, 17, 13, 22
    def __init__(self, m1F, m1B,  m2F, m2B, bool = False):
        if bool:  
            from gpiozero import PhaseEnableMotor as biMotor
            # from outputs.biMotor_bool import biMotor # using High Amperage driver
        else: 
            from gpiozero import Motor as biMotor
            # from outputs.biMotor import biMotor # using a L298 or similar driver
        self.motor1 = biMotor(m1F, m1B)
        self.motor2 = biMotor(m2F, m2B)
        self.right = 0
        self.left = 0
    
    def stop(self):
        # self.motor1.setSpeed(0)
        # self.motor2.setSpeed(0)
        self.motor1.stop()
        self.motor2.stop()
        
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
        # self.motor1.setSpeed(int(round(self.right)))
        # self.motor2.setSpeed(int(round(self.left)))
        if self.right > 0:
            self.motor1.forward(self.right/ 100.0)
        elif self.right < 0:
            self.motor1.backward(self.right * -0.01)
        else:
            self.motor1.stop()
        
        if self.left > 0:
            self.motor2.forward(self.left / 100.0)
        elif self.left < 0:
            self.motor2.backward(self.left * -0.01)
        else:
            self.motor2.stop()
        
    # for debugging purposes
    def print(self):
        print("left =", self.left)
        print("right =", self.right)
        
    def __del__(self):
        del self.motor1
        del self.motor2
#end drivetrain class

if __name__ == "__main__":
    import time
    d = drivetrain(17, 18, 22, 13)

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
