from outputs.rccartrain import cartrain
from outputs.drivetrain import drivetrain
import time


x = cartrain(17, 27, 22, 23)

x.drive(100, 0)
time.sleep(3)
x.drive(-100,0)
time.sleep(2)
x.drive(100, 3)
time.sleep(2)
x.drive(100, 0)


