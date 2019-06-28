# The MIT License (MIT)
#
# Copyright (c) 2017 Damien P. George
# Copyright (c) 2019 Rhys Thomas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_circuitpython_nrf24l01`
================================================================================

CircuitPython port of the nRF24L01 library from Micropython. Modified by Rhys
Thomas. Ported to work on the Raspberry Pi with Adafruit Blinka `SPI` and
`DigitalInOut` objects.

* Author(s): Damien P. George, Rhys Thomas

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/2bndy5/Adafruit_circuitpython_CircuitPython_nrf24l01.git"
import busio
from adafruit_bus_device.spi_device import SPIDevice
import time

# nRF24L01+ registers
CONFIG       = 0x00
EN_RXADDR    = 0x02
SETUP_AW     = 0x03
SETUP_RETR   = 0x04
RF_CH        = 0x05
RF_SETUP     = 0x06
STATUS       = 0x07
RX_ADDR_P0   = 0x0a
TX_ADDR      = 0x10
RX_PW_P0     = 0x11
FIFO_STATUS  = 0x17
DYNPD	     = 0x1c

# CONFIG register
EN_CRC       = 0x08 # enable CRC
CRCO         = 0x04 # CRC encoding scheme; 0=1 byte, 1=2 bytes
PWR_UP       = 0x02 # 1=power up, 0=power down
PRIM_RX      = 0x01 # RX/TX control; 0=PTX, 1=PRX

# RF_SETUP register
POWER_0      = 0x00 # -18 dBm
POWER_1      = 0x02 # -12 dBm
POWER_2      = 0x04 # -6 dBm
POWER_3      = 0x06 # 0 dBm
SPEED_1M     = 0x00
SPEED_2M     = 0x08
SPEED_250K   = 0x20

# STATUS register
RX_DR        = 0x40 # RX data ready; write 1 to clear
TX_DS        = 0x20 # TX data sent; write 1 to clear
MAX_RT       = 0x10 # max retransmits reached; write 1 to clear

# FIFO_STATUS register
RX_EMPTY     = 0x01 # 1 if RX FIFO is empty

# constants for instructions
R_RX_PL_WID  = 0x60 # read RX payload width
R_RX_PAYLOAD = 0x61 # read RX payload
W_TX_PAYLOAD = 0xa0 # write TX payload
FLUSH_TX     = 0xe1 # flush TX FIFO
FLUSH_RX     = 0xe2 # flush RX FIFO
NOP          = 0xff # use to read STATUS register

class NRF24L01(SPIDevice):
    def __init__(self, spi, csn, ce, channel=46, payload_size=32, baudrate=4000000, polarity=0, phase=0, extra_clocks=0):
        # max payload size is 32 bytes
        assert payload_size <= 32
        self.payload_size = payload_size
        # last address assigned to pipe0 for reading. init to None
        self.pipe0_read_addr = None
        
        # init the SPI bus and pins
        super(NRF24L01, self).__init__(spi, chip_select=csn, baudrate=baudrate, polarity=polarity, phase=phase, extra_clocks=extra_clocks)
        # init the buffer used to store data from spi transactions
        self.buf = bytearray(1)

        # store the ce pin
        self.ce = ce
        # reset ce.value & power up the chip
        self.ce.value = 0
        self.ce.value = 1
        # according to datasheet we must wait for pin to settle
        # this depends on the capacitor used on the VCC & GND 
        # assuming a 100nF (HIGHLY RECOMMENDED) wait time is slightly < 5ms
        time.sleep(0.005)
        with self:
            # set address width to 5 bytes and check for device present
            self._reg_write(SETUP_AW, 0b11)
            if self._reg_read(SETUP_AW) != 0b11:
                raise OSError("nRF24L01+ Hardware not responding")

            # disable dynamic payloads
            self._reg_write(DYNPD, 0)

            # auto retransmit delay: 1750us
            # auto retransmit count: 8
            self._reg_write(SETUP_RETR, (6 << 4) | 8)

            # clear status flags
            self._reg_write(STATUS, RX_DR | TX_DS | MAX_RT)

            # flush buffers
            self._flush_rx()
            self._flush_tx()

        # set rf power and speed
        self.set_power_speed(POWER_3, SPEED_250K) # Best for point to point links

        # init CRC
        self.set_crc(2)

        # set channel
        self.set_channel(channel)

    def _reg_read(self, reg):
        self.spi.readinto(self.buf, write_value=reg)
        self.spi.readinto(self.buf)
        return self.buf[0]

    def _reg_write_bytes(self, reg, buf):
        self.spi.readinto(self.buf, write_value=(0x20 | reg))
        self.spi.write(buf)
        return self.buf[0]

    def _reg_write(self, reg, value):
        self.spi.readinto(self.buf, write_value=(0x20 | reg))
        ret = self.buf[0]
        self.spi.readinto(self.buf, write_value=value)
        return ret

    def _flush_rx(self):
        self.spi.readinto(self.buf, write_value=FLUSH_RX)

    def _flush_tx(self):
        self.spi.readinto(self.buf, write_value=FLUSH_TX)

    # power is one of POWER_x defines; speed is one of SPEED_x defines
    def set_power_speed(self, power, speed):
        setup = self._reg_read(RF_SETUP) & 0b11010001
        self._reg_write(RF_SETUP, setup | power | speed)

    # length in bytes: 0, 1 or 2
    def set_crc(self, length):
        with self as spi:
            config = self._reg_read(CONFIG) & ~(CRCO | EN_CRC)
            if length == 0:
                pass
            elif length == 1:
                config |= EN_CRC
            else:
                config |= EN_CRC | CRCO
            self._reg_write(CONFIG, config)

    def set_channel(self, channel):
        with self:
            self._reg_write(RF_CH, min(channel, 125))

    # address should be a bytes object 5 bytes long
    def open_tx_pipe(self, address):
        assert len(address) == 5
        with self:
            self._reg_write_bytes(RX_ADDR_P0, address)
            self._reg_write_bytes(TX_ADDR, address)
            self._reg_write(RX_PW_P0, self.payload_size)

    # address should be a bytes object 5 bytes long
    # pipe 0 and 1 have 5 byte address
    # pipes 2-5 use same 4 most-significant bytes as pipe 1, plus 1 extra byte
    def open_rx_pipe(self, pipe_id, address):
        assert len(address) == 5
        assert 0 <= pipe_id <= 5
        with self:
            if pipe_id == 0:
                self.pipe0_read_addr = address
            if pipe_id < 2:
                self._reg_write_bytes(RX_ADDR_P0 + pipe_id, address)
            else:
                self._reg_write(RX_ADDR_P0 + pipe_id, address[0])
            self._reg_write(RX_PW_P0 + pipe_id, self.payload_size)
            self._reg_write(EN_RXADDR, self._reg_read(EN_RXADDR) | (1 << pipe_id))

    def start_listening(self):
        self.ce.value = 1
        time.sleep(0.00013)
        with self:
            self._reg_write(CONFIG, self._reg_read(CONFIG) | PWR_UP | PRIM_RX)
            self._reg_write(STATUS, RX_DR | TX_DS | MAX_RT)

            if self.pipe0_read_addr is not None:
                self._reg_write_bytes(RX_ADDR_P0, self.pipe0_read_addr)

            self.flush_rx()
            self.flush_tx()

    def stop_listening(self):
        with self:
            self.flush_tx()
            self.flush_rx()
        self.ce.value = 0

    # returns True if any data available to recv
    def any(self):
        with self: 
            return not bool(self._reg_read(FIFO_STATUS) & RX_EMPTY)

    def recv(self):
        with self as spi:
            # get the data
            spi.readinto(self.buf, write_value=R_RX_PAYLOAD)
            buf = spi.read(self.payload_size)
            # clear RX ready flag
            self._reg_write(STATUS, RX_DR)

            return buf

    # blocking wait for tx complete
    def send(self, buf, timeout=0.500):
        with self:
            self.send_start(buf)
            start = time.monotonic()
            result = None
            while result is None and (time.monotonic() - start) < timeout:
                result = self.send_done() # 1 == success, 2 == fail
            if result == 2:
                raise OSError("send failed")

    # non-blocking tx
    def send_start(self, buf):
        # power up
        self._reg_write(CONFIG, (self._reg_read(CONFIG) | PWR_UP) & ~PRIM_RX)
        time.sleep(0.00015)
        # send the data
        self.spi.readinto(self.buf, write_value=W_TX_PAYLOAD)
        self.spi.write(buf)
        if len(buf) < self.payload_size:
            self.spi.write(b'\x00' * (self.payload_size - len(buf))) # pad out data

        # enable the chip so it can send the data
        self.ce.value = 1
        time.sleep(0.000015) # needs to be >10us
        self.ce.value = 0

    # returns None if send still in progress, 1 for success, 2 for fail
    def send_done(self):
        if not (self._reg_read(STATUS) & (TX_DS | MAX_RT)):
            return None # tx not finished

        # either finished or failed: get and clear status flags, power down
        status = self._reg_write(STATUS, RX_DR | TX_DS | MAX_RT)
        self._reg_write(CONFIG, self._reg_read(CONFIG) & ~PWR_UP)
        return 1 if (status & TX_DS) else 2
