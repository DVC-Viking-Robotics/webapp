import time
# try:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False) # advised by useless debuggung prompts
# except ModuleNotFoundError:
#     # probably running on PC
#     pass
from gpiozero import DigitalOutputDevice, SourceMixin, CompositeDevice, GPIOThread

class Stepper(SourceMixin, CompositeDevice):
    def __init__(self, pins, speed = 60, stepType = 'half', maxSteps = 4069, DegreePerStep = 0.087890625, debug = False):
        self.maxSteps = maxSteps
        self.dps = DegreePerStep
        self.stepType = stepType
        self.debug = debug
        self.speed = speed
        self.dummy = False
        if len(pins) == 4:
            self.pins = pins
            try:
                for i in range(len(pins) - 1):
                    # GPIO.setup(pin, GPIO.OUT)
                    # GPIO.output(pin, False)
                    self.pins[i] = DigitalOutputDevice(pins[i])
            except NameError:
                self.dummy = True
        else:# did not pass exactly 4 gpio pins
            self.dummy = True
        self._it = 0 # iterator for rotating stepper
        # self._steps = steps specific to motor
        self.resetZeroAngle()
    
    def resetZeroAngle(self):
        self._steps = 0
    
    def step(self, dir = True):
        # increment or decrement step
        if dir: # going CW
            self._steps += 1
            self._it += 1
        else: # going CCW
            self._steps -= 1
            self._it -= 1
        # now check for proper range according to stepper type
        self.setPinState()

    def printDets(self):
        print('Angle:', self.angle, 'steps:', self._steps)

    def __clamp_it(self, max):
        if self._it > max - 1: self._it -= max
        elif self._it < 0: self._it += max

    def setPinState(self):
        if self.stepType == "half":
            maxStep = 8
            self.__clamp_it(maxStep)
            base = int(self._it / 2)
            next = base + 1
            if next == len(self.pins):
                next = 0
            for i in range(len(pins)):
                if i == base:
                    self.pins[i].on()
                elif i == next and self._it % 2 == 1:
                        self.pins[next].on()
                else:
                    self.pins[i].off()
        elif self.stepType == "full":
            maxStep = 4
            self.__clamp_it(maxStep)
            if self._it + 1 == maxStep: next = 0
            else: next = self._it + 1
            for i in range(len(pins) - 1):
                if i == self._it or i == next:
                    self.pins[i].on()
                else:
                    self.pins[i].off()
        elif self.stepType == "wave":
            maxStep = 4
            self.__clamp_it(maxStep)
            self.pins[self._it] = True
        else: # stepType specified is invalid
            errorPrompt = 'Invalid Stepper Type = ' + repr(self.stepType)
            raise RuntimeError(errorPrompt)

    def delay(self, speed):
        # delay between iterations based on motor speed (mm/sec)
        time.sleep(speed / 60000.0)

    def print(self):
        if self.debug or self.dummy:
            for pin in self.pin:
                print(int(pin.value), sep = '', end = '')
            print(' ')
            self.printDets()


    def wrapAngle(self, theta):
        """ 
        Ensure that argument 'theta' is kept accordingly within range [0,360]
        """
        while theta > 360 : theta -= 360
        while theta < 0 : theta += 360
        return theta
    
    def _stop_thread(self):
        if getattr(self, '_controller', None):
            self._controller._move_thread(self)
        self._controller = None
        if getattr(self, '_move_thread', None):
            self._move_thread.stop()
        self._move_thread = None
 
    def move2Angle(self, angle, isCCW, speed) :
        while abs(self.angle - angle) >= self.dps:
            # iterate self._steps
            self.step(isCCW)
            # write to pins
            self.setPinState()
            self.print()
            # wait a certain amount of time based on motor speed
            if not speed:
                self.delay(self.speed)
            else: 
                self.delay(speed)
    
    def moveSteps(self, numSteps, isCW, speed):
        while numSteps != 0:
            # iterate self._steps
            self.step(isCW)
            numSteps -= 1
            # write to pins
            self.setPinState()
            self.print()
            # wait a certain amount of time based on motor speed
            if not speed:
                self.delay(self.speed)
            else: 
                self.delay(speed)
    @property
    def angle(self):
        """
        Returns current angle of motor rotation [0,360]. Setting
        this property changes the state of the device.
        """
        return self.wrapAngle((self._steps % self.maxSteps) * self.dps)

    @angle.setter
    def angle(self, angle):
        # __clamp_it angle to constraints of [0,360] degrees
        angle = self.wrapAngle(angle)
        # decipher rotational direction
        dTccw = self.wrapAngle(self.angle - angle)
        dTcw = self.wrapAngle(angle - self.angle)
        if dTccw > dTcw: 
            isCCW = True
        else: isCCW = False
        self._stop_thread()
        self._move_thread = GPIOThread(
            target=self.move2Angle, args=(angle, isCCW, speed)
        )
        self._move_thread.start()
    
    @property
    def steps(self):
        """ 
        Returns counter of steps taken since instantiation or resetZeroAngle()
        """
        return self._steps

    @steps.setter
    def steps(self, numSteps):
        # decipher rotational direction
        if numSteps > 0 : isCW = True
        else: isCW = False
        # make numSteps positive for decrementing
        numSteps = abs(numSteps)
        self._stop_thread()
        self._move_thread = GPIOThread(
            target=self.move2Angle, args=(angle, isCCW, speed)
        )
        self._move_thread.start()
        

if __name__ == "__main__":
    m = Stepper((5,6,12,16))
    m.angle = -15
    # m.goSteps(64)
    time.sleep(2)
    m.angle = 15
    # m.goSteps(4096)
    time.sleep(2)
    # m.goSteps(-2048)
    m.angle = 0
    # time.sleep(2)
    # m.angle = 90

