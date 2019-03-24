import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts

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
    """
    this class definition uses the L293D IC to drive a single bidirectional motor
    note: each L293D IC can only drive up to 2 bidirectional motors
    """

    """
    see this post for GPIO pin number scheme:
    https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
    """
     

    #pass the GPIO pin numbers connecting to L293D input pins
    #example varName = bimotor(pin1, pin2) in main script
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
        
    #let finSpeed = target speed (-100 to 100)
    #let t = time to change(ramp) speed from initSpeed(current speed) to finSpeed
    def cellerate(self, finSpeed, t):
        finSpeed = max(-100, min(100, finSpeed)) # bounds check
        self.initSpeed = 0
        self.currSpeedF = self.pi.get_PWM_dutycycle(self.pinF)
        self.currSpeedB = self.pi.get_PWM_dutycycle(self.pinB)
        if self.currSpeedF > self.currSpeedB:
            self.initSpeed = self.currSpeedF
        else: self.initSpeed = self.currSpeedB * -1
        del self.currSpeedF, self.currSpeedB # clean temp vars
        # initial and destination speeds are now set [-100 to 100]
        """
        add code to ramp speed here
        requires multi-threading
        """

    #let x be the percentual target speed (in range of -100 to 100)
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

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pinF.stop()
        self.pinB.stop()
        del self.pinF
        del self.pinB

#end motor object
 