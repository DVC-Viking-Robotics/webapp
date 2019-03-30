import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts

class biMotor:
    """
    note: each "DROK DC 2-way H-Bridge Brush Motor Driver" can only drive up to 2 bidirectional motors
    """

    """
    see this post for GPIO pin number scheme:
    https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
    """
     

    #pass the GPIO pin numbers connecting to L293D input pins
    #example varName = bimotor(pin1, pin2) in main script
    def __init__(self, dirPin, pwmPin):
        GPIO.setup( pwmPin, GPIO.OUT)
        GPIO.setup(dirPin, GPIO.OUT)
        # variables used to track acceleration
        self.init_speed = 0
        self.dest_speed = 0
        # save pin numbers as GPIO.PWM objects
        self.dirPin = True
        self.pwmPin = GPIO.PWM(pwmPin, 15000)
        # start PWM signal
        self.pwmPin.start(0)
        #self.dirPin.start(0)  not needed

    #let x be the percentual target speed (in range of -100 to 100)
    def setSpeed(self, x):
        # check proper range of variable x
        x = max(-100, min(100, x))
        # going forward
        if x > 0: 
            self.pwmPin.ChangeDutyCycle(x)
            self.dirPin = True
        # going backward
        elif x < 0: 
            self.pwmPin.ChangeDutyCycle(x *-1)
            self.dirPin = False
        # otherwise stop
        else: 
            self.pwmPin.ChangeDutyCycle(0)
            self.dirPin = True

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pwmPin.stop()
        self.dirPin = False
        del self.pwmPin
        del self.dirPin

#end motor object



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
 