import math

class GPSnav:
    # def __init__(self, driveT, gpsIn):
    def __init__(self):
        self.waypoints = [{'lat': -122.07071872, 'lng': 37.96668393}, {'lat': -122.0711613, 'lng': 37.966604}]
        # self.d = driveT
        # self.gps = gpsIn
    
    def getNewHeading(self, base = 0):
        if len(self.waypoints) <= (base + 1): return 0
        else: # calc slope between 2 points and return as heading
            y2 = float(self.waypoints[base + 1]['lat'])
            x2 = float(self.waypoints[base + 1]['lng'])
            y1 = float(self.waypoints[base]['lat'])
            x1 = float(self.waypoints[base]['lng'])
            heading = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
            if y1 < 0:
                return heading * -1
            else: return heading


# self executable loop
if __name__ == "__main__":
    nav = GPSnav()
    print(nav.getNewHeading())