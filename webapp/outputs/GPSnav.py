import math
import time
class GPSnav:
    def __init__(self): # for testing heading calcs only
        self.waypoints = [{'lat': -122.07071872, 'lng': 37.96668393}, {'lat': -122.0711613, 'lng': 37.966604}]

    def __init__(self, driveT, imu, gps):
        self.waypoints = [{'lat': -122.0711613, 'lng': 37.966604}]
        self.d = driveT
        self.imu = imu
        self.gps = gps
    
    # override [] operators to return the waypoints queue
    def __getitem__(self, key):
        return self.waypoints[key]

    def __setitem__(self, key, val):
        raise RuntimeWarning('GPSnav.waypoints can not be directly set!! Use .insert() & .pop() accordingly!!')

    def insert(self, wp = None, index = -1):
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

    def printWP(self):
        for i in range(len(self.waypoints)):
            print(i + 1, 'lat =', self.waypoints[i]['lat'], 'lng =', self.waypoints[i]['lng'])

    def getNewHeading(self, currentPos, base = 0):
        
        if len(self.waypoints) == (base): 
            print("No GPS waypoints established.")
            return 0
        else: # calc slope between 2 points and return as heading
            y2 = float(self.waypoints[base]['lat'])
            x2 = float(self.waypoints[base]['lng'])
            y1 = float(currentPos['lat'])
            x1 = float(currentPos['lng'])

            #y1 = float(self.waypoints[base]['lat'])
            #x1 = float(self.waypoints[base]['lng'])
            heading = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
            if(heading < 0):
                heading+= 360
            return heading

    def alignHeading(self, heading):
        if self.d != None: 
            self.d.go(0,0)
            self.imu.heading = self.imu.get_all_data()
            print("current robot heading: ")
            print(self.imu.heading)

            dTcw = heading - self.imu.heading
            dTccw = self.imu.heading - heading
            if (dTcw < 0):
                dTcw +=360

            if (dTccw < 0):
                dTccw +=360

            if (dTcw < dTccw):
                self.d.go(15,0)
                print("turning clockwise")
            else:
                self.d.go(-15,0)
                print("turning counterclockwise")
            correctionAngle = 0
            self.d.go(0,0)
            self.imu.heading = self.imu.get_all_data()
            
            #correction angle based on how the mag3110 is mounted. edit value until 0 aligns robot with true north. 
            self.imu.heading += correctionAngle

            print("current robot heading: ")
            print(self.imu.heading)

            dTcw = heading - self.imu.heading
            dTccw = self.imu.heading - heading
            if (dTcw < 0):
                dTcw +=360

            if (dTccw < 0):
                dTccw +=360

            if (dTcw < dTccw):
                self.d.go(15,0)
                print("turning clockwise")
            else:
                self.d.go(-15,0)
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
            self.d.go(0,0)
            print("Coord reached")
# end GPSnav class

    def drivetoWaypoint(self):
        #retrieve the current position of the robot
        self.gps.getData(True)
        #NESW = {'lat': -122.07071872, 'lng': 37.96668393}
        NESW = {'lat': self.gps.NS, 'lng': self.gps.EW}
        #just making sure that the coordinates are getting stored properly
        print("current lat: ")
        print(self.waypoints[0]['lat'])
        print("current long: ")
        print(self.waypoints[0]['lng'])
        print("----------------")
        print("target lat: ")
        print(NESW['lat'])
        print("target long: ")
        print(NESW['lng'])
        
        #calculated the heading between current position and target coordinate (waypoint[0]['lat]['lng'])

        destinationHeading = self.getNewHeading(NESW)
        print("Destination heading =")
        print(destinationHeading)
        #turn the robot toward destination
        self.alignHeading(destinationHeading)
    
        #current position of the robot is stored in self.waypoints[base]['lat'] & self.waypoints[base]['lng']



# self executable loop
if __name__ == "__main__":
    nav = GPSnav()
    print(nav.getNewHeading())