""" this file has been depricated! only use if GPIOzero library is not available (for some reason), but 
NOTE there's no garantee it will work because its no longer tested"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts

class phasedMotor:
    #pass the GPIO pin numbers connecting to L293D input pins
    #example varName = bimotor(pin1, pin2) in main script
    def __init__(self, dirPin, pwmPin):
        GPIO.setup(pwmPin, GPIO.OUT)
        GPIO.setup(dirPin, GPIO.OUT)
        # variables used to track acceleration
        self.init_speed = 0
        self.dest_speed = 0
        # save pin numbers as GPIO.PWM objects
        self.dirPin = dirPin
        self.pwmPin = GPIO.PWM(pwmPin, 15000)
        # save pwm duty cyle as in [0,100] & start PWM signal
        self.pwm = 0
        self.pwmPin.start(self.pwm)
        self.dir = True
        self.smoothing_thread = None

    def _stopThread(self):
        if self.smoothing_thread is not None:
            self.smoothing_thread.join()
        self.smoothing_thread = None

    def _smooth(self, isUp, y0, dt):
        # delta_speed, instSpeed, self.finspeed, and y0 are all percentage [-1,1]
        # timeI & dt is in nanoseconds while isUp is a boolean [0 | 1]
        timeI = time.time_ns() - self.initSmooth
        while timeI < dt:
            delta_speed = sin( timeI / dt * math.pi / 2 + (-1 * isUp * math.pi / 2) ) + isUp 
            self.value = delta_speed * (self.finspeed - y0) + y0
            timeI = time.time_ns() - self.initSmooth

    #let finSpeed = target speed in range of [-1,1]
    #let deltaT = time in milliseconds to change/ramp speed from current speed(self.value) to finSpeed in range of [-1,1]
    def cellerate(self, finSpeed, deltaT = 1000):
        self.finSpeed = max(-100, min(100, round(finSpeed * 100))) # bounds check
        self.initSmooth = time.time_ns() # integer of nanoseconds
        self.finSmooth = self.initSmooth + deltaT * 1000 # integer = milliseconds * 1000 therfore nanoseconds
        baseSpeed = self.value 
        isUP = 1 if self.finSpeed > baseSpeed else 0
        self._stopThread()
        self.smoothing_thread = Thread(target=self._smooth, args=(isUP, baseSpeed, deltaT * 1000))
        self.smoothing_thread.start()

    #let x be the percentual target speed (in range of -100 to 100)
    @property
    def value(self):
        return self.pwm / 100.0 + int(self.dir) * -1

    @value.setter
    def value(self, x):
        # check proper range of variable x
        x = max(-100, min(100, x))
        # going forward
        if x > 0: 
            self.pwm = x
            self.dir = True
        # going backward
        elif x < 0: 
            self.pwm = x * -1
            self.dir = False
        # otherwise stop
        else: 
            self.pwm = 0
            self.dir = True
        self.pwmPin.ChangeDutyCycle(x)
        GPIO.output(self.dirPin, self.dir)

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pwmPin.stop()
        GPIO.output(self.dirPin, False)
        del self.pwmPin
        del self.dirPin
        GPIO.cleanup()

#end motor object 