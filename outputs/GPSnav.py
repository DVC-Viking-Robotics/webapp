import math

class GPSnav:
    def __init__(self): # for testing heading calcs only
        self.waypoints = [{'lat': -122.07071872, 'lng': 37.96668393}, {'lat': -122.0711613, 'lng': 37.966604}]

    def __init__(self, driveT, gpsIn):
        self.waypoints = []
        self.d = driveT
        self.gps = gpsIn
    
    def insert(self, index = -1, wp = None):
        if index < 0 or index > len(self.waypoints):
            # insert @ end of list if index is out of bounds
            self.waypoints.append(wp)
        else: # insert @ specified index
            self.waypoints.insert(index, wp)

    def pop(self, index = -1):
        # check bounds
        if index >= len(self.waypoints) or index < 0:
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
        if abs(heading - gps.heading) < abs(heading + 360 - gps.heading):
            #turn left
            self.d.go(0, -50)
        else: #turn right
            self.d.go(0, 50)
        while abs(gps.heading - heading) < 2:
            # hold steady until new heading is acheived w/in 2 degrees
            pass 
        d.go(0,0) #stop after alignment completes
# end GPSnav class

# self executable loop
if __name__ == "__main__":
    nav = GPSnav()
    print(nav.getNewHeading())