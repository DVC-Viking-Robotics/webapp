import time

class Stepper(object):
    def __init__(self, pins, speed = 60, stepType = 'wave', debug = False):
        self.stepType = stepType
        self.debug = debug
        self.speed = speed
        if len(pins) == 4:
            self.pins = pins
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False) # advised by useless debuggung prompts
                for pin in pins:
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, False)
            except ModuleNotFoundError:
                self.dummy = True
        else:# did not pass exactly 4 gpio pins
            self.dummy = True
        self.it = -1 # iterator for rotating stepper
        # self.steps = steps specific to motor
        self.setPinState()

    def resetPins(self):
        self.pinState = [False, False, False, False]
    
    def step(self, dir = True):
        # increment or decrement step
        if dir: self.it += 1 # going CW
        else: self.it -= 1   # going CCW
        # now check for proper range according to stepper type
        self.setPinState()

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
        else: # stepTyoe specified is invalid
            errorPrompt = 'Invalid Stepper Type = ' + repr(self.stepType)
            raise RuntimeError(errorPrompt)

    def delay(self):
        # delay between iterations based on set motor speed (mm/sec)
        time.sleep(self.speed / 60000.0)

    def write(self):
        if self.debug or self.dummy:
            for i in range(len(self.pinState)):
                print(int(self.pinState[i]), sep = '', end = '')
            print(' ')
        elif not self.dummy:
            for i in range(len(self.pins)):
                GPIO.output(self.pins[i], self.pinState[i])

    def go(self, numSteps):
        # decipher rotational direction
        if numSteps > 0: isCW = True
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
            self.delay()

if __name__ == "__main__":
    m = Stepper([1, 2], speed = 60, stepType = 'half')
    m.go(-10)
