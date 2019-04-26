from inputs.cmdArgs import args
cmd = args()

from inputs.IMU import LSM9DS1 as imu 
IMUsensor = imu(address = cmd['IMU']['address'].rsplit(','))

from outputs.Drivetrain import BiPed as drivetrain
d = drivetrain([18,17,13,22],0)


desiredHeading = 0
IMUsensor.get_all_data()
heading = IMUsensor.calcHeading()   

#turn the robot until the desired compas position is reached
while (heading != desiredHeading):
    
    IMUsensor.get_all_data()
    heading = IMUsensor.calcHeading()   
    print(heading)

    d.go(100,0)

#stop the motors once it exits the loop (the desired heading has been reached)
d.go(0,0)

