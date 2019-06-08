""" this file has been depricated! only use if GPIOzero library is not available (for some reason), but 
NOTE there's no garantee it will work because its no longer tested"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts
import time 
from threading import Thread

class biMotor:
    def __init__(self, pinB, pinF):
        GPIO.setup(pinF, GPIO.OUT)
        GPIO.setup(pinB, GPIO.OUT)
        # variables used to track acceleration
        self.init_speed = 0
        self.dest_speed = 0
        # save pin numbers as GPIO.PWM objects
        self.pinF = GPIO.PWM(pinF, 50)
        self.pinB = GPIO.PWM(pinB, 50)
        # save pwm duty cycles as int [0,100]
        self.pFor = 0
        self.pBac = 0
        # start PWM signal
        self.pinF.start(self.pFor)
        self.pinB.start(self.pBac)
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
       
    @property
    def value(self):
        return self.pFor - self.pBac / 100.0
    
    #let x be the percentual target speed in range of [-1,1]
    @value.setter
    def value(self, x):
        # check proper range of variable x
        x = max(-100, min(100, round(x * 100)))
        # going forward
        if x > 0: 
            self.pFor = x
            self.pBac = 0
        # going backward
        elif x < 0: 
            self.pFor = 0
            self.pBac = x * -1
        # otherwise stop
        else: 
            self.pFor = 0
            self.pBac = 0
        self.pinF.ChangeDutyCycle(self.pFor)
        self.pinB.ChangeDutyCycle(self.pBac)

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pinF.stop()
        self.pinB.stop()
        del self.pinF
        del self.pinB

#end motor object
 