# import libraries to read serial data coming from arduino (double heading value)
import time
import serial

ser = serial.Serial(
  port = '/dev/ttyUSB0',
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

#from inputs.IMU import LSM9DS1 as imu 
#IMUsensor = imu(address = cmd['IMU']['address'].rsplit(','))


#import drivetrain libraries to drive motors
from outputs.Drivetrain import BiPed as drivetrain
d = drivetrain([18,17,13,22],0)

#set desired heading value

desiredHeading = 0

while (1):
#turn the robot until the desired compas position is reached (range is used for accuracy loss) 

    turnToHeading(desiredHeading)

    #stop the motors once it exits the loop (the desired heading has been reached)
    print("desired heading received. 5 sec rest")
    d.go(0,0)
    time.sleep(5)



def turnToHeading(desiredHeading):
    
    heading = ser.readline()
    print("heading received")
    desiredHeadingMin = desiredHeading  - 5
    
    if (desiredHeadingMin < 0):
        desiredHeadingMin += 360

    desiredHeadingMax = desiredHeading + 5

    if (desiredHeadingMin > 360):
        desiredHeadingMin -= 360

    while (heading > desiredHeadingMax and heading < desiredHeadingMin):
        print("turning to heading")
        heading = ser.readline()
        print(heading)
        d.go(50,0)
    
    