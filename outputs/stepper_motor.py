"""
A driver class to implement the threaded module for unipolar stepper motors.
"""
import time
import math
from gpiozero import DigitalOutputDevice, SourceMixin, CompositeDevice
from gpiozero.threads import GPIOThread


class Stepper(SourceMixin, CompositeDevice):
    def __init__(self, pins=None, initial_angle=0.0, min_angle=-180, max_angle=180, speed=60, stepType='half', StepsPerRevolution=4069, DegreePerStep=0.087890625, pin_factory=None, verbose=False):
        self.SPR = StepsPerRevolution
        self.DPS = DegreePerStep
        self.stepType = stepType
        self.speed = speed
        self.pins = pins
        self.targetPos = None
        self.min_angle = min_angle
        self.max_angle = max_angle
        super(Stepper, self).__init__(pin_factory=pin_factory)
        if len(pins) == 4:
            self.pins = CompositeDevice(
                DigitalOutputDevice(pins[0], pin_factory=pin_factory),
                DigitalOutputDevice(pins[1], pin_factory=pin_factory),
                DigitalOutputDevice(pins[2], pin_factory=pin_factory),
                DigitalOutputDevice(pins[3], pin_factory=pin_factory),
                pin_factory=pin_factory)
        else:  # did not pass exactly 4 gpio pins
            raise RuntimeError(
                'pins passed to stepper must be an iterable list of exactly 4 numbers!')
        self._it = 0  # iterator for rotating stepper
        # self._steps = steps specific to motor
        self.resetZeroAngle()  # init self._steps = 0
        self._move_thread = None

    # override [] operators to return the CompositeDevice's list of DigitalOutputDevice(s)
    def __getitem__(self, key):
        return self.pins[key]

    def __setitem__(self, key, val):
        self.pins[key].value = bool(math.ceil(abs(val)))

    def resetZeroAngle(self):
        self._steps = 0

    def step(self, isCW=True):
        # increment or decrement step
        if isCW:  # going CW
            self._steps -= 1
            self._it -= 1
        else:  # going CCW
            self._steps += 1
            self._it += 1
        # now check for proper range according to stepper type

    def wrap_it(self, max, min=0, theta=None):
        """
        Ensure that argument 'theta' is kept accordingly within range [min,max]
        """
        if theta == None:
            theta = self._it
        while theta > max:
            theta -= max
        while theta < min:
            theta += max
        return theta

    def isCW(self):
        if self.targetPos == None and self.targetPos != self._steps:
            return None
        else:
            currPos = self.wrap_it(self.SPR, 0, self._steps % self.SPR)
            return self.wrap_it(self.SPR, 0, currPos - self.SPR / 2) < self.targetPos < currPos

    def write(self):
        if self.stepType == "half":
            maxStep = 8
            self._it = self.wrap_it(maxStep)
            base = int(self._it / 2)
            next = base + 1
            if next == len(self.pins):
                next = 0
            for i in range(len(self.pins)):
                if i == base or (i == next and self._it % 2 == 1):
                    self.pins[i].on()
                else:
                    self.pins[i].off()
        elif self.stepType == "full":
            maxStep = 4
            self._it = self.wrap_it(maxStep)
            if self._it + 1 == maxStep:
                next = 0
            else:
                next = self._it + 1
            for i in range(len(pins) - 1):
                if i == self._it or i == next:
                    self.pins[i].on()
                else:
                    self.pins[i].off()
        elif self.stepType == "wave":
            maxStep = 4
            self._it = self.wrap_it(maxStep)
            for i in range(len(pins) - 1):
                if i == self._it:
                    self.pins[i].on()
                else:
                    self.pins[i].off()
        else:  # stepType specified is invalid
            errorPrompt = 'Invalid Stepper Type = ' + repr(self.stepType)
            raise RuntimeError(errorPrompt)

    def delay(self):
        # delay between iterations based on motor speed (mm/sec)
        time.sleep(self.speed / 60000.0)

    def _getPinBin(self):
        pinBin = 0b0
        for i in range(len(self.pins)):
            pinBin |= (int(self.pins[i].value) << i)
        return pinBin

    def __repr__(self):
        output = 'pins = {} Angle: {} Steps: {}'.format(
            bin(self._getPinBin()), repr(self.angle), repr(self.steps))
        return output

    def _stop_thread(self):
        if getattr(self, '_move_thread', None):
            self._move_thread.stop()
        self._move_thread = None

    def moveSteps(self):
        while self.targetPos != None and self._steps != self.targetPos:
            print(self._steps, '!=', self.targetPos)
            # iterate self._steps
            self.step(self.isCW())
            # write to pins
            self.write()
            # wait a certain amount of time based on motor speed
            self.delay()

    @property
    def angle(self):
        """
        Returns current angle of motor rotation [0,360]. Setting
        this property changes the state of the device.
        """
        return self.wrap_it(360, 0, (self._steps % self.SPR) * self.DPS)

    @angle.setter
    def angle(self, angle):
        """
        Rotate motor to specified angle where direction is
        automatically detirmined toward the shortest route.
        All input angle is valid since it is wrapped to range [0,360]. *see wrap_it()
        """
        # wrap_it angle to constraints of [0,360] degrees
        angle = self.wrap_it(360, 0, angle)
        self.targetPos = None
        self._stop_thread()
        self.targetPos = round(angle / self.DPS)
        print('targetPos =', self.targetPos)
        self._move_thread = GPIOThread(target=self.moveSteps)
        self._move_thread.start()

    @property
    def steps(self):
        """
        Returns counter of steps taken since instantiation or resetZeroAngle()
        """
        return self._steps

    @steps.setter
    def steps(self, numSteps):
        """
        Task motor to execute specified numSteps where direction is the +/- sign on the numSteps variable
        """
        self.targetPos = None
        self._stop_thread()
        self.targetPos = self.wrap_it(self.SPR, 0, numSteps)
        print('targetPos =', self.targetPos)
        self._move_thread = GPIOThread(target=self.moveSteps)
        self._move_thread.start()

    @property
    def is_active(self):
        """
        Returns :data:`True` if the motor is currently running and
        :data:`False` otherwise.
        """
        if self._move_thread != None:
            return not self._move_thread._is_stopped
        else:
            return False

    @property
    def value(self):
        """
        Returns the percent angle of the motor.
        """
        return (self._steps % self.SPR) / self.SPR

    @value.setter
    def value(self, value):
        """
        Sets the percent angle of the motor in range [-180,180].
        Valid input value is in range [-1,1]
        """
        if value is None:
            self.resetZeroAngle()
        elif -1 <= value <= 1:
            self.targetPos = None
            self._stop_thread()
            self.targetPos = self.wrap_it(self.SPR, 0, self.SPR / 2 * value)
            print('targetPos =', self.targetPos)
            self._move_thread = GPIOThread(target=self.moveSteps)
            self._move_thread.start()
        else:
            raise OutputDeviceBadValue(
                "stepper value must be between -1 and 1, or None")


if __name__ == "__main__":
    from gpiozero.pins.mock import MockFactory
    mockpins = MockFactory()
    m = Stepper([5, 6, 12, 16], pin_factory=mockpins)
    m.angle = -15
    # m.steps = 64
    time.sleep(1)
    print(repr(m))
    m.value = 0.5
    # m.angle = 15
    # m.steps = 500
    time.sleep(2)
    print(repr(m))
    # m.steps = -512
    m.angle = 0
    time.sleep(1)
    print(repr(m))
