from gpiozero import MCP3008

class adc:
    def __init__(self):
        self.ADC = [MCP3008(0), MCP3008(1), MCP3008(2), MCP3008(3), MCP3008(4), MCP3008(5). MCP3008(6), MCP3008(7)]
        self.values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.get_dist_data()

    def get_dist_data(self):
        for i in range(len(self.ADC)):
            self.values[i] = self.ADC[i].value
    
    '''
    maybe add some other functions for calibration
    the MCP3008 class looks promising
    https://gpiozero.readthedocs.io/en/stable/api_spi.html#mcp3008
    '''