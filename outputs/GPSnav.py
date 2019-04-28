import math

class GPSnav:
    def __init__(self): # for testing heading calcs only
        self.waypoints = [{'lat': -122.07071872, 'lng': 37.96668393}, {'lat': -122.0711613, 'lng': 37.966604}]

    def __init__(self, driveT, imu):
        self.waypoints = []
        self.d = driveT
        self.imu = imu
    
    def insert(self, index = -1, wp = None):
        if index < 0 or index > len(self.waypoints):
            # insert @ end of list if index is out of bounds
            self.waypoints.append(wp)
        else: # insert @ specified index
            self.waypoints.insert(index, wp)

    def pop(self, index = -1):
        # check bounds
        if index >= len(self.waypoints) or index < -1:
            return None # do nothing if out of bounds
        else: return self.waypoints.pop(index)

    def clear(self):
       self.waypoints.clear()
    
    def len(self):
        return len(self.waypoints)

    def getNewHeading(self, base = 0):
        if len(self.waypoints) <= (base + 1): return 0
        else: # calc slope between 2 points and return as heading
            y2 = float(self.waypoints[base + 1]['lat'])
            x2 = float(self.waypoints[base + 1]['lng'])
            y1 = float(self.waypoints[base]['lat'])
            x1 = float(self.waypoints[base]['lng'])
            heading = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
            return heading

    def alignHeading(self, heading):
        
        self.imu.heading = self.imu.get_all_data()
        print(self.imu.heading)

        dTcw = heading - self.imu.heading
        dTccw = self.imu.heading - heading
        if (dTcw < 0):
            dTcw +=360

        if (dTccw < 0):
            dTccw +=360

        if (dTcw < dTccw):
            self.d.go(8,0)
            print("turning clockwise")
        else:
            self.d.go(-8,0)
            print("turning counterclockwise")



            """  if abs(heading - self.imu.heading) < abs(heading + 360 - self.imu.heading):
            print("Left turn")
            #turn left
            self.d.go(-5, 0)
            else: #turn right
            print("Right turn")
            self.d.go(5, 0) """

        while abs(self.imu.heading - heading) > 6.5:
            print("Turning")
            # hold steady until new heading is acheived w/in 2 degrees
            self.imu.heading = self.imu.get_all_data()
            print(self.imu.heading)
        self.d.go(0,0) #stop after alignment completes
        print("Coord reached")
# end GPSnav class

# self executable loop
if __name__ == "__main__":
    nav = GPSnav()
    print(nav.getNewHeading())