import math

class GPSnav:
    def __init__(self, driveT, gpsIn):
        self.waypoints = []
        self.d = driveT
        self.gps = gpsIn
    
    def getNewHeading(self):
        if len(self.waypoints) == 0: return 0
        else: # calc slope between 2 points and return as heading
            myloc = self.gps.getData()
            x1 = float(myloc['lat'])
            x2 = float(self.waypoints[0]['lat'])
            y1 = float(myloc['lng'])
            y2 = float(self.waypoints[0]['lng'])
            m =  (y2 - y1) / (x2 - x1)
            return math.degrees(math.tan(m))


# self executable loop
if __name__ == "__main__":
    pass