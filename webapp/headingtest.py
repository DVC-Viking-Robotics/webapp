
# pylint: disable=invalid-name,missing-docstring

# import libraries to read serial data coming from arduino (double heading value)
import time
import board
from drivetrain.drivetrain import Tank, BiMotor
import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# use drivetrain libraries to drive motors
motors = [BiMotor([board.D18, board.D17]), BiMotor([board.D13, board.D22])]
d_train = Tank(motors, 85)

# set desired heading value here
target_heading = 0.0  # always north

course_heading = 0.0
time.sleep(0.1)
ser.readline()


def turnToHeading(desired_heading):

    heading = float(ser.readline().decode('utf-8'))
    print("heading received")
    print(heading)

    # desired_headingMin = desired_heading  - 4

    # if (desired_headingMin < 0):
    #     desired_headingMin += 360

    # desired_headingMax = desired_heading + 4

    # if (desired_headingMax > 360):
    #     desired_headingMax -= 360

    while abs(heading - desired_heading) > 10:
        print("turning to heading")

        dTcw = desired_heading - heading
        dTccw = heading - desired_heading
        if dTcw < 0:
            dTcw += 360

        if dTccw < 0:
            dTccw += 360

        if dTcw < dTccw:
            d_train.go(10, 0)
            print("turning clockwise")
        else:
            d_train.go(-10, 0)
            print("turning counterclockwise")

        heading = float(ser.readline().decode('utf-8'))
        print(heading)


while 1:
    # turn the robot until the desired compas position is reached (range is used for accuracy loss)

    turnToHeading(target_heading)
    # (ser.readline().decode('utf-8'))
    # stop the motors once it exits the loop (the desired heading has been reached)
    print("Desired heading achieved. Old Keith gotta take a rest")
    ser.flush()
    course_heading = float(ser.readline().decode('utf-8'))

    # I DONT KNOW HOW TO GIVE KEITH A BREAK BECAUSE SERIAL BUFFER WONT CLEAR. *cry*
    d_train.go(0, 0)
