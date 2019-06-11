import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts
import time
from threading import Thread
import math

class Solonoid(object):
    def __init__(self, pins, rampTime = 100):
        self.signals = []
        self.pins = []
        for pin in pins:
            # save pwm duty cycles as int [0,100]; direction signals will be treated like bool [0|1]
            self.signals.append(0)
            GPIO.setup(pin, GPIO.OUT)
        # variables used to track acceleration
        self.finSpeed = 0
        self.initSmooth = 0
        self.finSmooth = 0
        self.smoothing_thread = None
        self.TBC = False
        self._dt = rampTime # time in milliseconds to change/ramp speed from self.value to self.finSpeed

    def _stopThread(self):
        if self.smoothing_thread is not None:
            self.smoothing_thread.join()
        self.smoothing_thread = None

    def _smooth(self):
        """ 
        delta_speed, self.finSpeed, and self.initSpeed are all percentage [-1,1]
        timeI & dt is in microseconds
        """
        timeI = int(time.monotonic() * 1000) - self.initSmooth
        while timeI < (self.finSmooth - self.initSmooth) and self.TBC:
            # print('time:', timeI, 'delta_t:', self.finSmooth - self.initSmooth)
            delta_speed = 1 - math.cos(timeI / float(self.finSmooth - self.initSmooth) * math.pi / 2)
            # print('delta_s:', delta_speed, '= 1 - cos(', timeI / float(self.finSmooth - self.initSmooth), '*PI/2)')
            # print('pwm:', (delta_speed * (self.finSpeed - self.initSpeed) + self.initSpeed) / 100.0, '= (', delta_speed, '* (', self.finSpeed, '-', self.initSpeed, ') +', self.initSpeed, ') / 100.0')
            self.value = (delta_speed * (self.finSpeed - self.initSpeed) + self.initSpeed) / 100.0
            time.sleep(0.001) # sleep 1 ms
            timeI = int(time.monotonic() * 1000) - self.initSmooth
        self.value = self.finSpeed / 100.0

    # let finSpeed be the percentual target speed [-1,1]
    def cellerate(self, finSpeed):
        """ 
        let finSpeed = target speed in range of [-1,1]
        let deltaT = percent [0,1] of delta time (self._dt in milliseconds)
        """
        self.finSpeed = max(-100, min(100, round(finSpeed * 100))) # bounds check
        self.initSmooth = int(time.monotonic() * 1000) # integer of milliseconds
        self.initSpeed = int(self.value * 100)
        deltaT = abs((self.finSpeed - self.initSpeed) / 200.0)
        # self.finSmooth = self.initSmooth + self._dt
        self.finSmooth = self.initSmooth + deltaT * self._dt
        self.TBC = False
        self._stopThread()
        self.smoothing_thread = Thread(target=self._smooth)
        self.TBC = True
        self.smoothing_thread.start()

    @property
    def value(self):
            return int(self.signals[0]) or (int(self.signals[1]) if len(pins) > 1 else 0)

    @value.setter
    def value(self, x):
        # check proper range of variable x [-1,1]
        x = max(-100, min(100, round(x * 100)))
        # going forward
        if x > 0: 
            self.signals[0] = True
            if len(self.pins) > 1:
                self.signals[1] = False
        # going backward
        elif x < 0: 
            self.signals[0] = False
            if len(self.pins) > 1:
                self.signals[1] = True
        # otherwise stop
        else: 
            self.signals[0] = False
            if len(self.pins) > 1:
                self.signals[1] = False
        GPIO.output(self.pins[0], self.signals[0])
        if len(self.pins) > 1:
            GPIO.output(self.pins[1], self.signals[1])


    def __del__(self):
        if self.smoothing_thread is not None:
            self.smoothing_thread._stop()
        
# end Solonoid parent class

class BiMotor(Solonoid):
    def __init__(self, pins, rampTime = 1000):
        super(BiMotor, self).__init__(pins, rampTime)
        # save pin numbers as GPIO.PWM objects
        for i in range(len(pins)):
            self.pins.append(GPIO.PWM(pins[i], 50))
            self.pins[i].start(self.signals[i])

    @property
    def value(self):
        return (self.signals[0] - (self.signals[1] if len(self.signals) > 1 else 0)) / 100.0
    
    #let x be the percentual target speed in range of [-1,1]
    @value.setter
    def value(self, x):
        # check proper range of variable x
        x = max(-100, min(100, round(x * 100)))
        # going forward
        if x > 0: 
            self.signals[0] = x
            if len(self.pins) > 1:
                self.signals[1] = 0
        # going backward
        elif x < 0: 
            self.signals[0] = 0
            if len(self.pins) > 1:
                self.signals[1] = x * -1
        # otherwise stop
        else: 
            self.signals[0] = 0
            if len(self.pins) > 1:
                self.signals[1] = 0
        self.pins[0].ChangeDutyCycle(self.signals[0])
        if len(self.pins) > 1:
            self.pins[1].ChangeDutyCycle(self.signals[1])

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pins[0].stop()
        if len(self.pins) > 1:
            self.pins[1].stop()
        super(BiMotor, self).__del__()
# end BiMotor child class

class PhasedMotor(Solonoid):
    def __init__(self, pins, rampTime = 1000):
        super(PhasedMotor, self).__init__(pins, rampTime)
        # save pin number as GPIO.PWM objects
        self.pins.append(GPIO.PWM(pins[0], 15000))
        self.pins[0].start(self.signals[0]) # start pwm signal
        if len(pins) >= 1:
            # save direction signal pin # & set coresponding signal value to true
            self.pins.append(pins[1])
            self.signals[1] = True

    #let x be the percentual target speed (in range of -100 to 100)
    @property
    def value(self):
        if len(pins) > 1:
            return self.signals[0] / 100.0 * (1 if bool(self.signals[1]) else -1)
        else: return self.signals[0] / 100.0

    @value.setter
    def value(self, x):
        # check proper range of variable x
        x = max(-100, min(100, round(x * 100)))
        # going forward
        if x > 0: 
            self.signals[0] = x
            if len(self.pins) > 1:
                self.signals[1] = True
        # going backward
        elif x < 0: 
            self.signals[0] = x * -1
            if len(self.pins) > 1:
                self.signals[1] = False
        # otherwise stop
        else: 
            self.signals[0] = 0.0
            if len(self.pins) > 1:
                self.signals[1] = True
        self.pins[0].ChangeDutyCycle(self.signals[0])
        if len(self.pins) > 1:
            GPIO.output(self.pins[1], self.signals[1])

    #destructor to disable GPIO.PWM operation
    def __del__(self):
        self.pins[0].stop()
        if len(self.pins) > 1:
            GPIO.output(self.pins[1], False)
        super(PhasedMotor, self).__del__()
#end PhasedMotor child class 

if __name__ == "__main__":
    m = BiMotor([18, 17])
    m.value = 0
    m.cellerate(1.0)
    time.sleep(1)
    print(m.value)
    m.cellerate(-1.0)
    time.sleep(2)
    print(m.value)
    m.cellerate(0.0)
    time.sleep(1)
    print(m.value)