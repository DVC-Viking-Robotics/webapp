import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # advised by useless debuggung prompts
            
class Stepper(object):
    def __init__(self, pins, speed = 60, stepType = 'half', DegreePerStep = 0.087890625, debug = False):
        self.dps = DegreePerStep
        self.stepType = stepType
        self.debug = debug
        self.speed = speed
        self.dummy = False
        if len(pins) == 4:
            self.pins = pins
            try:
                for pin in pins:
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, False)
            except NameError:
                self.dummy = True
        else:# did not pass exactly 4 gpio pins
            self.dummy = True
        self.it = 0 # iterator for rotating stepper
        # self.steps = steps specific to motor
        self.setPinState()
        self.angle = 0
        self.steps = 0

    def resetPins(self):
        self.pinState = [False, False, False, False]
    
    def step(self, dir = True):
        # increment or decrement step
        if dir: # going CW
            self.steps += 1
            self.it += 1
        else: # going CCW
            self.steps -= 1
            self.it -= 1
        # now check for proper range according to stepper type
        self.setPinState()
        self.angle = self.steps * self.dps
        self.print()

    def print(self):
        print('Angle:', self.angle, 'steps:', self.steps)

    def clamp(self, max):
        if self.it > max - 1: self.it -= max
        elif self.it < 0: self.it += max

    def setPinState(self):
        self.resetPins()
        if self.stepType == "half":
            maxStep = 8
            self.clamp(maxStep)
            base = int(self.it / 2)
            self.pinState[base] = True
            if self.it % 2 == 1: 
                next = base + 1
                if next == len(self.pinState):
                    next = 0
                self.pinState[next] = True
        elif self.stepType == "full":
            maxStep = 4
            self.clamp(maxStep)
            if self.it + 1 == maxStep: next = 0
            else: next = self.it + 1
            self.pinState[self.it] = True
            self.pinState[next] = True
        elif self.stepType == "wave":
            maxStep = 4
            self.clamp(maxStep)
            self.pinState[self.it] = True
        else: # stepType specified is invalid
            errorPrompt = 'Invalid Stepper Type = ' + repr(self.stepType)
            raise RuntimeError(errorPrompt)

    def delay(self, speed):
        # delay between iterations based on motor speed (mm/sec)
        time.sleep(speed / 60000.0)

    def write(self):
        if self.debug or self.dummy:
            for pin in self.pinState:
                print(int(pin), sep = '', end = '')
            print(' ')
        elif not self.dummy:
            GPIO.output(self.pins, self.pinState)
        
    def goAngle(self, angle, speed = None):
        # clamp angle to constraints of 0-360 degrees
        angle = min(360, max(-360, angle))
        # decipher rotational direction
        if abs(angle - self.angle) > abs(self.angle - angle) : 
            isCW = True
        else: isCW = False
        while abs(self.angle - angle) > self.dps * 2:
            # iterate self.steps
            self.step(isCW)
            # write to pins
            self.write()
            # wait a certain amount of time based on motor speed
            if not speed:
                self.delay(self.speed)
            else: 
                self.delay(speed)
            
        
    def goSteps(self, numSteps, speed = None):
            # decipher rotational direction
            if numSteps > 0 : isCW = True
            else: isCW = False
            # make numSteps positive for decrementing
            numSteps = abs(numSteps)
            while numSteps != 0:
                # iterate self.steps
                self.step(isCW)
                numSteps -= 1
                # write to pins
                self.write()
                # wait a certain amount of time based on motor speed
                if not speed:
                    self.delay(self.speed)
                else: 
                    self.delay(speed)

if __name__ == "__main__":
    m = Stepper([5,6,12,16])
    m.goAngle(-90)
    time.sleep(2)
    m.goAngle(-270)
    time.sleep(2)
    m.goAngle(0)
    time.sleep(2)
    m.goAngle(90)

