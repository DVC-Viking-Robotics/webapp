# import libraries to read serial data coming from arduino (double heading value)
import time
import serial

ser = serial.Serial(
  port = 'COM11',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

#from inputs.IMU import LSM9DS1 as imu 
#IMUsensor = imu(address = cmd['IMU']['address'].rsplit(','))


#import drivetrain libraries to drive motors
#from outputs.Drivetrain import BiPed as drivetrain
#d = drivetrain([18,17,13,22],0)

#set desired heading value


desiredHeading = 340.0
heading = 0.0
time.sleep(0.1) 
ser.readline()

def turnToHeading(desiredHeading):
    
    heading = float(ser.readline().decode('utf-8'))
    print("heading received")
    print(heading)
    
    desiredHeadingMin = desiredHeading  - 5
    
    if (desiredHeadingMin < 0):
        desiredHeadingMin += 360

    desiredHeadingMax = desiredHeading + 5

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
            #d.go(50,0)
            print("turning clockwise")
        else:
            #d.go(-50,0)
            print("turning counterclockwise")

        heading = float(ser.readline().decode('utf-8'))
        print(heading)
        


while (1):
#turn the robot until the desired compas position is reached (range is used for accuracy loss) 

    turnToHeading(desiredHeading)
    #(ser.readline().decode('utf-8'))
    #stop the motors once it exits the loop (the desired heading has been reached)
    print("desired heading received. 5 sec rest")
    ser.flush()
    heading = float(ser.readline().decode('utf-8'))
    
    
    #d.go(0,0)
   

    
    