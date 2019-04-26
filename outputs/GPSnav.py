class GPSnav:
    def __init__(self, driveT, gpsIn):
        self.waypoints = []
        self.d = driveT
        self.gps = gpsIn
    
    def getNewHeading(self):
        if len(self.waypoints) == 0: return 0
        else: # calc slope between 2 points and return as heading
            myloc = self.gps.getData()
            x1 = float(self.waypoints[0]['lat'])
            x2 = float(myloc['lat'])
            y1 = float(self.waypoints[0]['lng'])
            y2 = float(myloc['lng'])
            return (y1 - y2) / (x1 - x2)


# self executable loop
if __name__ == "__main__":
    pass