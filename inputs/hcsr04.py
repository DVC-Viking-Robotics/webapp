from gpiozero import DistanceSensor


class hcsr04:
    def __init__(self):
        self.HCSR04 = [
            DistanceSensor(5, 6), 
            DistanceSensor(12, 16), 
            DistanceSensor(19, 26), 
            DistanceSensor(20, 21)]

    # key is an int in range [0,3]
    def __getattribute__(self, key):
        assert 0 <= key <= 3
        return self.HCSR04[key]

    '''
    maybe set some other functions for calibration
    GPIOzero MCP3008 library has some promising features
    https://gpiozero.readthedocs.io/en/stable/api_input.html#distancesensor-hc-sr04
    '''
