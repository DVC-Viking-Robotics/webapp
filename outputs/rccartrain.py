# this class serves to drive the motors on a cheap chinese car 
# with directional servo GPIO. Motor and servo layout: 

#           (wheel) MOTOR1 (wheel) 
#             ------servo------
#
#           (wheel) MOTOR2 (wheel)

# Car is all-wheel drive but left an right wheel work in coordination

#class constructor: x = drive(in1, in2, in3, in4) -> BOARD PINS 


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class cartrain:
    #initialize all GPIO pins
    def __init__(self, in1, in2, in3, in4):
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)

        self.pwm1 = GPIO.PWM(in1, 50)
        self.pwm2 = GPIO.PWM(in2, 50)
        self.pwm3 = GPIO.PWM(in3, 50)
        self.pwm4 = GPIO.PWM(in4, 50)

        self.pwm1.start(0)
        self.pwm2.start(0)
        self.pwm3.start(0)
        self.pwm4.start(0)

    def drive(self, x, y): 
        # control the servo motor for the given x direction 
        #input is x directino from -100 to 100 
        # when x is -100, need to reverse direction of servo 
        #motor to given value
        if x > 0:
            self.pwm3.changeDutyCycle(0)
            self.pwm4.changeDutyCycle(x)
        elif x < 0: 
            self.pwm3.changeDutyCycle(abs(x))
            self.pwm4.changeDutyCycle(0)
        else: 
            self.pwm3.changeDutyCycle(0)
            self.pwm4.changeDutyCycle(0)

        if y > 0: 
            self.pwm1.changeDutyCycle(0)
            self.pwm2.changeDutyCycle(y)

        elif y < 0: 
            self.pwm1.changeDutyCycle(abs(y))
            self.pwm2.changeDutyCycle(0)
        else:
            self.pwm1.changeDutyCycle(0)
            self.pwm2.changeDutyCycle(0)
        





  


