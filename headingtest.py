# import libraries to read serial data coming from arduino (double heading value)
import time
import serial

ser = serial.Serial(
  port = '/dev/ttyUSB0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

#import drivetrain libraries to drive motors
from outputs.Drivetrain import BiPed as drivetrain
d = drivetrain([18,17,13,22],0)

#set desired heading value here
desiredHeading = 0.0 #always north

heading = 0.0
time.sleep(0.1) 
ser.readline()

def turnToHeading(desiredHeading):
    
    heading = float(ser.readline().decode('utf-8'))
    print("heading received")
    print(heading)
    
    desiredHeadingMin = desiredHeading  - 10
    
    if (desiredHeadingMin < 0):
        desiredHeadingMin += 360

    desiredHeadingMax = desiredHeading + 10

    if (desiredHeadingMax > 360):
        desiredHeadingMax -= 360

    while ((heading > desiredHeadingMax) or (heading < desiredHeadingMin)):
        print("turning to heading")

        dTcw = desiredHeading - heading
        dTccw = heading - desiredHeading 
        if (dTcw < 0):
            dTcw +=360

        if (dTccw < 0):
            dTccw +=360

        if (dTcw < dTccw):
            d.go(5,0)
            print("turning clockwise")
        else:
            d.go(-5,0)
            print("turning counterclockwise")

        heading = float(ser.readline().decode('utf-8'))
        print(heading)
        


while (1):
#turn the robot until the desired compas position is reached (range is used for accuracy loss) 

    turnToHeading(desiredHeading)
    #(ser.readline().decode('utf-8'))
    #stop the motors once it exits the loop (the desired heading has been reached)
    print("Desired heading achieved. Old Keith gotta take a rest")
    ser.flush()
    heading = float(ser.readline().decode('utf-8'))
    
    #I DONT KNOW HOW TO GIVE KEITH A BREAK BECAUSE SERIAL BUFFER WONT CLEAR. *cry*
    d.go(0,0)
   

    
    