
'''

# test code forward reverse.
#import wiringpi
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin1 = 17
pin2 = 18
pin3 = 22
pin4 = 13


#motor nr 1
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
#motor nr 2
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

#spin the motors forward at full speed

#motor 1
GPIO.output(pin1,GPIO.HIGH)
pwm1 = GPIO.PWM(pin2, 15000) #pin 27, at frequency of 50 Hz
pwm1.start(0)
pwm1.ChangeDutyCycle(100)
#motor2
GPIO.output(pin3,GPIO.HIGH)
pwm2 = GPIO.PWM(pin4, 15000) #pin 27, at frequency of 50 Hz
pwm2.start(0)
pwm2.ChangeDutyCycle(100)

'''

from outputs.newbiMotor import biMotor
class drivetrain:
      
    #using BCM pins 17, 18, 22, 13
    def __init__(self, m1F, m1B,  m2F, m2B):
        self.motor1 = biMotor(m1F, m1B)
        self.motor2 = biMotor(m2F, m2B)
        self.right = 0
        self.left = 0
    
    def stop(self):
        self.motor1.setSpeed(0)
        self.motor2.setSpeed(0)
        
    # pass backwards/forward (-100 to 100) as variable x
    # pass left/right (-100 to 100) as variable y
    def go(self, x, y):
        # make sure arguments are in their proper range
        x = int(round(max(-100, min(100, x))))
        y = int(round(max(-100, min(100, y))))
        # set the axis directly to their corresponding motors
        self.right = y
        self.left = x
        self.motor1.setSpeed(self.right)
        self.motor2.setSpeed(self.left)
    
    # for debugging purposes
    def print(self):
        print("left =", self.left)
        print("right =", self.right)
        
    def __del__(self):
        del self.motor1
        del self.motor2
        GPIO.cleanup()

#end drivetrain class

if __name__ == "__main__":
    import time
    d = drivetrain(17, 27, 22, 23)

    d.go(100, 0)
    time.sleep(2)
    d.go(0, 100)
    time.sleep(2)
    d.go(100, 100)
    time.sleep(2)
    d.go(-100, 0)
    time.sleep(2)
    d.go(0, -100)
    time.sleep(2)
    d.go(-100, -100)
    time.sleep(2)
    d.stop()

    del d

