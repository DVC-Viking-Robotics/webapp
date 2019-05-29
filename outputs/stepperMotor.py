import time
import math
from gpiozero import DigitalOutputDevice, SourceMixin, CompositeDevice, BadPinFactory
from gpiozero.threads import GPIOThread

class Stepper(SourceMixin, CompositeDevice):
    def __init__(self, pins, speed = 60, stepType = 'half', maxSteps = 4069, DegreePerStep = 0.087890625):
        self.maxSteps = maxSteps
        self.dps = DegreePerStep
        self.stepType = stepType
        self.speed = speed
        self.dummy = False
        self.pins = pins
        super(Stepper, self).__init__()
        if len(pins) == 4:
            try:
                self.pins = CompositeDevice(
                    DigitalOutputDevice(pins[0]), DigitalOutputDevice(pins[1]), DigitalOutputDevice(pins[2]), DigitalOutputDevice(pins[3]))
            except BadPinFactory:
                self.dummy = True
                self.pins[i] = False
        else:# did not pass exactly 4 gpio pins
            self.dummy = True
        self._it = 0 # iterator for rotating stepper
        # self._steps = steps specific to motor
        self.resetZeroAngle()
        self._move_thread = None
 
    # override [] operators to return the CompositeDevice's list of DigitalOutputDevice(s)
    def __getitem__(self, key):
        return self.pins[key]

    def __setitem__(self, key, val):
        self.pins[key].value = bool(math.ceil(abs(val)))

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
        # self.setPinState()

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
            for i in range(len(self.pins)):
                if i == base or (i == next and self._it % 2 == 1):
                    if self.dummy:
                        self.pins[i] = True
                    else: self.pins[i].on()
                else:
                    if self.dummy:
                        self.pins[i] = False
                    else: self.pins[i].off()        
        elif self.stepType == "full":
            maxStep = 4
            self.__clamp_it(maxStep)
            if self._it + 1 == maxStep: next = 0
            else: next = self._it + 1
            for i in range(len(pins) - 1):
                if i == self._it or i == next:
                    if self.dummy:
                        self.pins[i] = True
                    else: self.pins[i].on()
                else:
                    if self.dummy:
                        self.pins[i] = False
                    else: self.pins[i].off()        
        elif self.stepType == "wave":
            maxStep = 4
            self.__clamp_it(maxStep)
            for i in range(len(pins) - 1):
                if i == self._it:
                    if self.dummy:
                        self.pins[i] = True
                    else: self.pins[i].on()
                else:
                    if self.dummy:
                        self.pins[i] = False
                    else: self.pins[i].off()        
        else: # stepType specified is invalid
            errorPrompt = 'Invalid Stepper Type = ' + repr(self.stepType)
            raise RuntimeError(errorPrompt)

    def delay(self, speed):
        # delay between iterations based on motor speed (mm/sec)
        time.sleep(speed / 60000.0)

    def _getPinBin(self):
        pinBin = 0b0
        for i in range(len(self.pins)):
            if not self.dummy:
                pinBin |= (int(self.pins[i].value) << i)
            else:
                pinBin |= (int(self.pins[i]) << i)
        return format(pinBin, 'b')
            
    def print(self):
        if self.dummy:
            print(self._getPinBin())
            self.printDets()


    def wrapAngle(self, theta):
        """ 
        Ensure that argument 'theta' is kept accordingly within range [0,360]
        """
        while theta > 360 : theta -= 360
        while theta < 0 : theta += 360
        return theta
    
    def _stop_thread(self):
        if getattr(self, '_move_thread', None):
            self._move_thread.stop()
        self._move_thread = None
 
    def move2Angle(self, angle, isCCW) :
        while abs(self.angle - angle) >= self.dps:
            # iterate self._steps
            self.step(isCCW)
            # write to pins
            self.setPinState()
            self.print()
            # wait a certain amount of time based on motor speed
            self.delay(self.speed)
            
        
    def moveSteps(self, numSteps, isCW):
        while numSteps != 0:
            # iterate self._steps
            self.step(isCW)
            numSteps -= 1
            # write to pins
            self.setPinState()
            self.print()
            # wait a certain amount of time based on motor speed
            self.delay(self.speed)

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
        try:
            self._move_thread = Thread(target=self.move2Angle, args=(angle, isCCW))
        except NameError:
            self._move_thread = GPIOThread(target=self.move2Angle, args=(angle, isCCW))
        finally:
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
            target=self.moveSteps, args=(numSteps, isCW)
        )
        self._move_thread.start()
    
    @property
    def value(self):
        """
        Returns binary number representing the pins (pin1 = LSB ... pin4 = MSB). Setting
        this property changes the percent angle of the motor.
        """
        return _getPinBin()

    @value.setter
    def value(self, value):
        if value is None:
            self.resetZeroAngle()
        elif -1 <= value <= 1:
            self.angle = value * 180.0 / self.dps
        else:
            raise OutputDeviceBadValue(
                "stepper value must be between -1 and 1, or None")
        

if __name__ == "__main__":
    m = Stepper([5,6,12,16])
    m.angle = -15
    # m.goSteps(64)
    time.sleep(2)
    m.angle = 15
    # m.goSteps(4096)
    time.sleep(2)
    # m.goSteps(-2048)
    m.angle = 0
    time.sleep(2)
    # m.angle = 90

