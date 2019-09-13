import pigpio

class ADC:
    """
    class for gathering data from MCP3002, MCP3004, or MCP3008 via pigpio
    """
    def __init__(self, CS):
        self.pi = pigpio.pi()
        # check for proper chip select AKA the 'CE#' pin where # is 0 | 1 
        CS = max(0, min(1, CS))
        # create handle for use with pigpio spi functions
        self.adc = self.pi.spi_open(CS, 50000)

    def mcp3002(self, channel, debug = False):
        # check proper range for analog channel (0 or 1 on MCP3002)
        channel = max(0, min(1, channel))
        # gather data after sending data. *see spi_xfer(args) and MCP3002 datasheet
        self.result = self.pi.spi_xfer(self.adc, [1, (2 + channel) << 6, 0])
        if debug: self.printRawResult(self.result)
        # return data from chip
        return (self.result[1][1] << 8) + self.result[1][2]
    # end read mcp3002

    def mcp3004(self, channel, debug = False):
        # check proper range for analog channel (0 to 3 on MCP3004)
        channel = max(0, min(3, channel))
        # gather data after sending data. *see spi_xfer(args) and MCP3004 datasheet
        self.result = self.pi.spi_xfer(self.adc, [1, (8 + channel) << 4, 0])
        if debug: self.printRawResult(self.result)
        # return data from chip
        return (self.result[1][1] << 8) + self.result[1][2]
    # end mcp3008

    def mcp3008(self, channel, debug = False):
        # check proper range for analog channel (0 to 7 on MCP3008)
        channel = max(0, min(7, channel))
        # gather data after sending data. *see spi_xfer(args) and MCP3008 datasheet
        self.result = self.pi.spi_xfer(self.adc, [1, (8 + channel) << 4, 0])
        if debug: self.printRawResult(self.result)
        # return data from chip
        return (self.result[1][1] << 8) + self.result[1][2]
    # end mcp3008

    def printRawResult(self, r):
        '''
        for debug purposes
        '''
        print(r[0], 'bytes =', end = ' ')
        for i in range(r[0]):
            print(bin(r[1][i]), end = ' ')
        print() # finish debug output with '\n'

    def __del__(self):
        self.pi.spi_close(self.adc)
        self.pi.stop()
        del self.pi
# end class ADC

# for testing. Adjust to suit your IC model (e.g. mcp3008 vs mcp3002)
if __name__ == "__main__":
    adc = ADC(0)
    print('channel 1 =', adc.mcp3008(0, debug = True))
    print('channel 2 =', adc.mcp3008(1, debug = True))
    print('channel 3 =', adc.mcp3008(2, debug = True))
    print('channel 4 =', adc.mcp3008(3, debug = True))
    print('channel 5 =', adc.mcp3008(4, debug = True))
    print('channel 6 =', adc.mcp3008(5, debug = True))
    print('channel 7 =', adc.mcp3008(6, debug = True))
    print('channel 8 =', adc.mcp3008(7, debug = True))
    del adc