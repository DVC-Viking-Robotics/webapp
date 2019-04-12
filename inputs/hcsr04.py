from gpiozero import DistanceSensor
    
class hcsr04:
    def __init__(self):
        self.HCSR04 = [DistanceSensor(5, 6), DistanceSensor(12, 16), DistanceSensor(19, 26), DistanceSensor(20, 21)]
        self.values = [0.0, 0.0, 0.0, 0.0]
        self.get_dist_data()

    def get_dist_data(self):
        for i in range(len(self.HCSR04)):
            self.values[i] = self.HCSR04[i].value
    '''
    maybe set some other functions for calibration
    GPIOzero MCP3008 library has some promising features
    https://gpiozero.readthedocs.io/en/stable/api_input.html#distancesensor-hc-sr04
    '''
