import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

"""
important info from datasheet
L293D input pins: 2,7,10,15
L293D output pins: 3,6,11,14
L293D pins to pull high to enable: 1 enables pins 2-8, 9 enables 10-16
L293D power pins: 8 powers motors (<36V @ 600mA cont.), 16 powers IC (4.5-7V)
input pins can be pulled high by jumping wires from pin 16 to pins 1 and/or 9
remember to connect ground to the following pins: 4,5,12,13
"""

class biMotor:

    def __init__(self, pinF, pinB):
        GPIO.setup(pinF, GPIO.OUT)
        GPIO.setup(pinB, GPIO.OUT)
        # variables used to track acceleration
        self.init_speed = 0
        self.dest_speed = 0
        # save pin numbers as GPIO.PWM objects
        self.pinF = GPIO.PWM(pinF, 50)
        self.pinB = GPIO.PWM(pinB, 50)
        # start PWM signal
        self.pinF.start(0)
        self.pinB.start(0)

    def setSpeed(self, x):
        # check proper range of variable x
        x = max(-100, min(100, x))
        # going forward
        if x > 0: 
            self.pinF.ChangeDutyCycle(x)
            self.pinB.ChangeDutyCycle(0)
        # going backward
        elif x < 0: 
            self.pinF.ChangeDutyCycle(0)
            self.pinB.ChangeDutyCycle(x *-1)
        # otherwise stop
        else: 
            self.pinF.ChangeDutyCycle(0)
            self.pinB.ChangeDutyCycle(0)


class drivetrain:
      
    #using BCM pins 17, 27, 22, 23
    def __init__(self, m1F, m1B,  m2F, m2B):
        self.motor1 = biMotor(m1F, m1B)
        self.motor2 = biMotor(m2F, m2B)
        self.right = 0
        self.left = 0
    
    def stop(self):
        self.motor1.setSpeed(0)
        self.motor2.setSpeed(0)
        
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
            if y > 0:
                self.right = x * ((100 - y) / 100.0)
            elif y < 0:
                self.left = x * ((-100 - y) / 100.0) * -1
        # make sure speeds are an integer (not decimal/float) and send to motors
        self.motor1.setSpeed(int(round(self.right)))
        self.motor2.setSpeed(int(round(self.left)))



""" example of how to use in main script:

from drivetrain import drivetrain
d = drivetrain(17, 27, 22, 23)

d.go(75, 0)
time.sleep(8)
d.go(0, 75)
time.sleep(3.19)
d.go(75, 75)
time.sleep(3.19)
d.stop()

del d
"""