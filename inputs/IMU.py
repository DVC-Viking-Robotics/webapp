import smbus
import time

Gravity = 9.80665

const_LSM9DS1 = {
    "ADDRESS_XLG"            : 0x6a,
    "ADDRESS_MAG"            : 0x1c,
    "XG_ID"                  : 0b01101000,
    "MAG_ID"                 : 0b00111101,
    "ACCEL_MG_LSB_2G"        : 0.061,
    "ACCEL_MG_LSB_4G"        : 0.122,
    "ACCEL_MG_LSB_8G"        : 0.244,
    "ACCEL_MG_LSB_16G"       : 0.732,
    "MAG_MGAUSS_4GAUSS"      : 0.14,
    "MAG_MGAUSS_8GAUSS"      : 0.29,
    "MAG_MGAUSS_12GAUSS"     : 0.43,
    "MAG_MGAUSS_16GAUSS"     : 0.58,
    "GYRO_DPS_DIGIT_245DPS"  : 0.00875,
    "GYRO_DPS_DIGIT_500DPS"  : 0.01750,
    "GYRO_DPS_DIGIT_2000DPS" : 0.07000,
    "TEMP_LSB_DEGREE_CELSIUS": 8, # 1°C = 8, 25° = 200, etc.
    "WHO_AM_I_XG"   : 0x0F,
    "CTRL_REG1_G"   : 0x10,
    "CTRL_REG2_G"   : 0x11,
    "CTRL_REG3_G"   : 0x12,
    "TEMP_OUT_L"    : 0x15,
    "TEMP_OUT_H"    : 0x16,
    "STATUS_REG"    : 0x17,
    "OUT_X_L_G"     : 0x18,
    "OUT_X_H_G"     : 0x19,
    "OUT_Y_L_G"     : 0x1A,
    "OUT_Y_H_G"     : 0x1B,
    "OUT_Z_L_G"     : 0x1C,
    "OUT_Z_H_G"     : 0x1D,
    "CTRL_REG4"     : 0x1E,
    "CTRL_REG5_XL"  : 0x1F,
    "CTRL_REG6_XL"  : 0x20,
    "CTRL_REG7_XL"  : 0x21,
    "CTRL_REG8"     : 0x22,
    "CTRL_REG9"     : 0x23,
    "CTRL_REG10"    : 0x24,
    "OUT_X_L_XL"    : 0x28,
    "OUT_X_H_XL"    : 0x29,
    "OUT_Y_L_XL"    : 0x2A,
    "OUT_Y_H_XL"    : 0x2B,
    "OUT_Z_L_XL"    : 0x2C,
    "OUT_Z_H_XL"    : 0x2D,
    "WHO_AM_I_M"    : 0x0F,
    "CTRL_REG1_M"   : 0x20,
    "CTRL_REG2_M"   : 0x21,
    "CTRL_REG3_M"   : 0x22,
    "CTRL_REG4_M"   : 0x23,
    "CTRL_REG5_M"   : 0x24,
    "STATUS_REG_M"  : 0x27,
    "OUT_X_L_M"     : 0x28,
    "OUT_X_H_M"     : 0x29,
    "OUT_Y_L_M"     : 0x2A,
    "OUT_Y_H_M"     : 0x2B,
    "OUT_Z_L_M"     : 0x2C,
    "OUT_Z_H_M"     : 0x2D,
    "CFG_M"         : 0x30,
    "INT_SRC_M"     : 0x31,
    # "SENSORS_GRAVITY_STANDARD"  : 9.80665,
    # User facing constants/module globals.
    "XL_RANGE_2G"   : (0b00 << 3),
    "XL_RANGE_16G"  : (0b01 << 3),
    "XL_RANGE_4G"   : (0b10 << 3),
    "XL_RANGE_8G"   : (0b11 << 3),
    "M_GAIN_4GAUSS" : (0b00 << 5),  # +/- 4 gauss
    "M_GAIN_8GAUSS" : (0b01 << 5),  # +/- 8 gauss
    "M_GAIN_12GAUSS": (0b10 << 5),  # +/- 12 gauss
    "M_GAIN_16GAUSS": (0b11 << 5),  # +/- 16 gauss
    "G_SCALE_245DPS": (0b00 << 3),  # +/- 245 degrees/s rotation
    "G_SCALE_500DPS": (0b01 << 3),  # +/- 500 degrees/s rotation
    "G_SCALE_2000DPS": (0b11 << 3)  # +/- 2000 degrees/s rotation
}

const_MPU6050 = {
    # Scale Modifiers
    "ACCEL_SCALE_MODIFIER_2G"    : 16384.0,
    "ACCEL_SCALE_MODIFIER_4G"    : 8192.0,
    "ACCEL_SCALE_MODIFIER_8G"    : 4096.0,
    "ACCEL_SCALE_MODIFIER_16G"   : 2048.0,
    "GYRO_SCALE_MODIFIER_250DEG" : 131.0,
    "GYRO_SCALE_MODIFIER_500DEG" : 65.5,
    "GYRO_SCALE_MODIFIER_1000DEG": 32.8,
    "GYRO_SCALE_MODIFIER_2000DEG": 16.4,
    # Pre-defined ranges
    "ACCEL_RANGE_2G"       : 0x00,
    "ACCEL_RANGE_4G"       : 0x08,
    "ACCEL_RANGE_8G"       : 0x10,
    "ACCEL_RANGE_16G"      : 0x18,
    "GYRO_RANGE_250DEG"    : 0x00,
    "GYRO_RANGE_500DEG"    : 0x08,
    "GYRO_RANGE_1000DEG"   : 0x10,
    "GYRO_RANGE_2000DEG"   : 0x18,
    # MPU-6050 Registers
    "PWR_MGMT_1"    : 0x6B,
    "PWR_MGMT_2"    : 0x6C,
    "ACCEL_XOUT0"   : 0x3B,
    "ACCEL_YOUT0"   : 0x3D,
    "ACCEL_ZOUT0"   : 0x3F,
    "TEMP_OUT0"     : 0x41,
    "GYRO_XOUT0"    : 0x43,
    "GYRO_YOUT0"    : 0x45,
    "GYRO_ZOUT0"    : 0x47,
    "ACCEL_CONFIG"  : 0x1C,
    "GYRO_CONFIG"   : 0x1B,
}

class IMU(object):
    def __init__(self, address = (0x6a, 0x1C), bus = 1):
        # Class-level buffer for reading and writing data with the sensor.
        # This reduces memory allocations but means the code is not re-entrant or
        # thread safe!
        self.buf = bytearray(6)
        # instantiate I2C bus 1 for the raspberry pi
        self.bus = smbus.SMBus(bus)

    def readRaw(self, addy, reg):
        return self.bus.read_i2c_block_data(addy, reg)

    def _twos_comp(self, val, bits):
        # Convert an unsigned integer in 2's compliment form of the specified bit
        # length to its signed integer value and return it.
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val

class LSM9DS1(IMU):
    """Driver for the LSM9DS1 accelerometer, magnetometer, gyroscope."""

    def __init__(self, address = (0x6a, 0x1C), bus = 1):
        super(LSM9DS1, self).__init__()
        try:
            # Check ID registers.
            if self.bus.read_byte_data(address[0], const_LSM9DS1["WHO_AM_I_XG"]) == const_LSM9DS1["XG_ID"] and self.bus.read_byte_data(address[1], const_LSM9DS1["WHO_AM_I_M"]) == const_LSM9DS1["MAG_ID"]:
                const_LSM9DS1["ADDRESS_XLG"] = address[0]
                const_LSM9DS1["ADDRESS_MAG"] = address[1]
        except IOError:
            raise RuntimeError('Could not find LSM9DS1 @ address', repr(bytes(address)),', check wiring!')

        # soft reset & reboot accel/gyro
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG8"], 0x05)
        # soft reset & reboot magnetometer
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["CTRL_REG2_M"], 0x0C)
        time.sleep(0.01)
        # enable gyro continuous
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG1_G"], 0xC0) # on XYZ
        # Enable the accelerometer continous
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG5_XL"], 0x38)
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG6_XL"], 0xC0)
        # enable mag continuous
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["CTRL_REG3_M"], 0x00)
        # read biases and store ranges accordingly
        self.get_gyro_range()
        self.get_accel_range()
        self.get_mag_gain()

    def get_accel_range(self):
        reg = self.bus.read_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG6_XL"])
        val = reg & 0b00011000
        if val == const_LSM9DS1["XL_RANGE_2G"]:
            self._accel_mg_lsb = const_LSM9DS1["ACCEL_MG_LSB_2G"]
        elif val == const_LSM9DS1["XL_RANGE_4G"]:
            self._accel_mg_lsb = const_LSM9DS1["ACCEL_MG_LSB_4G"]
        elif val == const_LSM9DS1["XL_RANGE_8G"]:
            self._accel_mg_lsb = const_LSM9DS1["ACCEL_MG_LSB_8G"]
        elif val == const_LSM9DS1["XL_RANGE_16G"]:
            self._accel_mg_lsb = const_LSM9DS1["ACCEL_MG_LSB_16G"]
        return reg

    def set_accel_range(self, val):
        """The accelerometer range.  Must be a value of:
          val must be = 2,4,8, or 16 (units: G)
        """
        reg = self.get_accel_range()
        if const_LSM9DS1.get('XL_RANGE_' + val + 'G') != None:
            self._accel_mg_lsb = const_LSM9DS1.get('ACCEL_MG_LSB_' + val + 'G')
            val = const_LSM9DS1.get('XL_RANGE_' + val + 'G')
        else: 
            print('range ', val, 'G is undefined. using 2', sep = '')
            val = const_LSM9DS1["XL_RANGE_2G"]
            self._accel_mg_lsb = const_LSM9DS1["ACCEL_MG_LSB_2G"]
        reg |= val
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG6_XL"], reg)

    def get_mag_gain(self):
        reg = self.bus.read_byte_data(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["CTRL_REG2_M"])
        val = reg & 0b01100000
        if val == const_LSM9DS1["M_GAIN_4GAUSS"]:
            self._mag_mgauss_lsb = const_LSM9DS1["MAG_MGAUSS_4GAUSS"]
        elif val == const_LSM9DS1["M_GAIN_8GAUSS"]:
            self._mag_mgauss_lsb = const_LSM9DS1["MAG_MGAUSS_8GAUSS"]
        elif val == const_LSM9DS1["M_GAIN_12GAUSS"]:
            self._mag_mgauss_lsb = const_LSM9DS1["MAG_MGAUSS_12GAUSS"]
        elif val == const_LSM9DS1["M_GAIN_16GAUSS"]:
            self._mag_mgauss_lsb = const_LSM9DS1["MAG_MGAUSS_16GAUSS"]
        return reg

    def set_mag_gain(self, val):
        """The magnetometer gain.  Must be a value of:
          val must be = 4,8,12, or 16 (units: GAUSS)
        """
        reg = self.get_mag_gain()
        if const_LSM9DS1.get('M_GAIN_' + val + 'GAUSS') != None:
            self._mag_mgauss_lsb = const_LSM9DS1.get("MAG_MGAUSS_" + val + "GAUSS")
            val = const_LSM9DS1.get('M_GAIN_' + val + 'GAUSS')
        else: 
            print('gain:', val, 'GAUSS is undefined. using 4')
            self._mag_mgauss_lsb = const_LSM9DS1.get("MAG_MGAUSS_" + val + "GAUSS")
            val = const_LSM9DS1.get('M_GAIN_4GAUSS')
            return
        reg |= val
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["CTRL_REG2_M"], reg)
        # self.bus.write_byte_data(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["CTRL_REG2_M"], 0x0C)
        # time.sleep(0.01)
        
    def get_gyro_range(self):
        reg = self.bus.read_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG1_G"])
        val = reg & 0b00011000
        if val == const_LSM9DS1["G_SCALE_245DPS"]:
            self._gyro_dps_digit = const_LSM9DS1["GYRO_DPS_DIGIT_245DPS"]
        elif val == const_LSM9DS1["G_SCALE_500DPS"]:
            self._gyro_dps_digit = const_LSM9DS1["GYRO_DPS_DIGIT_500DPS"]
        elif val == const_LSM9DS1["G_SCALE_2000DPS"]:
            self._gyro_dps_digit = const_LSM9DS1["GYRO_DPS_DIGIT_2000DPS"]
        return reg

    def set_gyro_range(self, val):
        """The gyroscope scale.  Must be a value of:
          val must be = 245, 500, or 2000 (units: DPS)
        """
        reg = self.get_gyro_range()
        if const_LSM9DS1.get('G_SCALE_' + val + 'DPS') != None:
            val = const_LSM9DS1.get('G_SCALE_' + val + 'DPS')
        else: 
            print('scale: ', val, 'Deg/s is undefined. using 245', sep = '')
            val = const_LSM9DS1.get('G_SCALE_245DPS')
            self._gyro_dps_digit = const_LSM9DS1["GYRO_DPS_DIGIT_245DPS"]
        reg |= val
        self.bus.write_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["CTRL_REG1_G"], reg)

    def read_accel_raw(self):
        """Read the raw accelerometer sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values"""
        # Read the accelerometer
        self.buf = self.readRaw(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["OUT_X_L_XL"])
        return self.axisTuple(self.buf[0:6])

    def get_accel_data(self):
        """The accelerometer X, Y, Z axis values as a 3-tuple of
        m/s^2 values.
        """
        accel = self.read_accel_raw()
        accel = (accel[0] * self._accel_mg_lsb / 1000.0 * Gravity, accel[1] * self._accel_mg_lsb / 1000.0 * Gravity, accel[2] * self._accel_mg_lsb / 1000.0 * Gravity)
        return accel

    def read_mag_raw(self):
        """Read the raw magnetometer sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values"""
        # Read the magnetometer
        self.buf = self.readRaw(const_LSM9DS1["ADDRESS_MAG"], const_LSM9DS1["OUT_X_L_M"])
        return self.axisTuple(self.buf[0:6])

    def get_mag_data(self):
        """The magnetometer X, Y, Z axis values as a 3-tuple of
        gauss values.
        """
        mag = self.read_mag_raw()
        mag = (mag[0] * self._mag_mgauss_lsb / 1000.0, mag[1] * self._mag_mgauss_lsb / 1000.0, mag[2] * self._mag_mgauss_lsb / 1000.0)
        return mag

    def read_gyro_raw(self):
        """Read the raw gyroscope sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values"""
        # Read the gyroscope
        self.buf = self.readRaw(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["OUT_X_L_G"])
        return self.axisTuple(self.buf[0:6])

    def get_gyro_data(self):
        """The gyroscope X, Y, Z axis values as a 3-tuple of
        degrees/second values.
        """
        gyro = self.read_gyro_raw()
        gyro = (gyro[0] * self._gyro_dps_digit, gyro[1] * self._gyro_dps_digit, gyro[2] * self._gyro_dps_digit)
        return gyro

    def read_temp_raw(self):
        """Read the raw temperature sensor value and return it as a 12-bit
        signed value.  If you want the temperature in nice units you probably
        want to use the temperature property!
        """
        # Read temp sensor
        return self._twos_comp(self.bus.read_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["TEMP_OUT_L"]) | ( (self.bus.read_byte_data(const_LSM9DS1["ADDRESS_XLG"], const_LSM9DS1["TEMP_OUT_H"]) & 0x0F) << 8 ), 12)

    def get_temp(self):
        """The temperature of the sensor in degrees Celsius."""
        # This is just a guess since the starting point (21C here) isn't documented :(
        # See discussion from:
        #  https://github.com/kriswiner/LSM9DS1/issues/3
        return 27.5 + self.read_temp_raw() / 16
 
    def get_all_data(self):
        """Reads and returns all the available data."""
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()
        mag = self.get_mag_data()
        return [accel, gyro, mag]

    def axisTuple(self, buff):
        x = (buff[1] << 8) | buff[0]
        y = (buff[3] << 8) | buff[2]
        z = (buff[5] << 8) | buff[4]
        return (self._twos_comp(x, 16), self._twos_comp(y, 16), self._twos_comp(z, 16))

class MPU6050(IMU):
    def __init__(self, address = (0x68), bus=1):
        super(MPU6050, self).__init__(bus)
        self.address = address
        # Wake up the MPU-6050 since it starts in sleep mode
        try:
            self.bus.write_byte_data(self.address, const_MPU6050["PWR_MGMT_1"], 0x00)
        except IOError:
            raise RuntimeError('Could not find the GY-521 @ address', repr(address),', check your wiring')
        self.get_accel_range()
        self.get_gyro_range()
            
    def read_temp_raw(self):
        return self._twos_comp(self.bus.read_byte_data(self.address, const_MPU6050["TEMP_OUT0"] + 1) | (self.bus.read_byte_data(self.address, const_MPU6050["TEMP_OUT0"]) << 8 ), 16)

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.

        Returns the temperature in degrees Celcius.
        
        Get the actual temperature using the formule given in the
        MPU-6050 Register Map and Descriptions revision 4.2, page 30
        raw_temp = self.read_temp_raw()
        actual_temp = raw_temp / 340.0 + 36.53
        """
        return self.read_temp_raw() / 340.0 + 36.53

    def get_accel_range(self):
        """Reads the range the accelerometer is set to"""
        raw = self.bus.read_byte_data(self.address, const_MPU6050["ACCEL_CONFIG"]) & 0x18
        if raw == const_MPU6050["ACCEL_RANGE_2G"]:
            self.accel_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_2G"]
        elif raw == const_MPU6050["ACCEL_RANGE_4G"]:
            self.accel_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_4G"]
        elif raw == const_MPU6050["ACCEL_RANGE_8G"]:
            self.accel_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_8G"]
        elif raw == const_MPU6050["ACCEL_RANGE_16G"]:
            self.accel_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_16G"]

    def set_accel_range(self, val):
        """Sets the range of the accelerometer to range.
        val must be = 2, 4, 8, or 16 (units: Gauss)
        """
        if const_MPU6050.get('ACCEL_RANGE_' + val + 'G') != None:
            self.gyro_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_" + val + "G"]
            val =  const_MPU6050.get('ACCEL_RANGE_' + val + 'G')
        else:
            print('range:', val, 'G undefined. using 2')
            self.gyro_scale_modifier = const_MPU6050["ACCEL_SCALE_MODIFIER_2G"]
            val =  const_MPU6050.get('ACCEL_RANGE_2G')
        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, const_MPU6050["ACCEL_CONFIG"], val)

    def get_gyro_range(self):
        """Reads the range the gyroscope is set to"""
        raw = self.bus.read_byte_data(self.address, const_MPU6050["GYRO_CONFIG"]) & 0x18
        if raw == const_MPU6050["GYRO_RANGE_250DEG"]:
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_250DEG"]
        elif raw == const_MPU6050["GYRO_RANGE_500DEG"]:
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_500DEG"]
        elif raw == const_MPU6050["GYRO_RANGE_1000DEG"]:
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_1000DEG"]
        elif raw == const_MPU6050["GYRO_RANGE_2000DEG"]:
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_2000DEG"]
        
    def set_gyro_range(self, val):
        """Sets the range of the gyroscope to range.
        val must be = 250, 500, 1000, 2000 (units: DEG/sec)
        """
        if const_MPU6050.get('GYRO_RANGE_' + val + 'DEG') != None:
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_" + val + "DEG"]
            val =  const_MPU6050.get('GYRO_RANGE_' + val + 'DEG')
        else:
            print('range:', val, 'Deg/s undefined. using 250')
            self.gyro_scale_modifier = const_MPU6050["GYRO_SCALE_MODIFIER_250DEG"]
            val =  const_MPU6050.get('GYRO_RANGE_250DEG')
        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, const_MPU6050["GYRO_CONFIG"], val)

    def read_accel_raw(self):
        """Read the raw accelerometer sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values"""
        self.buf = self.readRaw(self.address, const_MPU6050['ACCEL_XOUT0'])
        return self.axisTuple(self.buf[0:6])

    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        """
        self.get_accel_range()
        accel = self.read_accel_raw()
        accel = (accel[0] / self.accel_scale_modifier, accel[1] / self.accel_scale_modifier, accel[2] / self.accel_scale_modifier)

        if not g:
            accel = (accel[0] * Gravity, accel[1] * Gravity, accel[2] * Gravity)
        return accel

    def read_gyro_raw(self):
        """Read the raw gyroscope sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values"""
        self.buf = self.readRaw(self.address, const_MPU6050['GYRO_XOUT0'])
        return self.axisTuple(self.buf[0:6])

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope"""
        self.get_gyro_range()
        gyro = self.read_gyro_raw()
        gryo = (gyro[0] / self.gyro_scale_modifier, gyro[1] / self.gyro_scale_modifier, gyro[2] / self.gyro_scale_modifier)
        return gyro

    def get_all_data(self):
        """Reads and returns all the available data."""
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()

        return [accel, gyro]

    def axisTuple(self, buff):
        x = (buff[0] << 8) | buff[1]
        y = (buff[2] << 8) | buff[3]
        z = (buff[4] << 8) | buff[5]
        return (self._twos_comp(x, 16), self._twos_comp(y, 16), self._twos_comp(z, 16))

if __name__ == "__main__":
    import os
    import argparse
    #add description to program's help screen
    parser = argparse.ArgumentParser(description='testing purposes. Please try using quotes to encompass values. ie "COM5" or "/dev/ttyS0"')
    parser.add_argument('--dof', default='6', help='Select # Degrees Of Freedom. 6 = the GY-521 board. 9 = the LSM9DS1 board. Any additionally comma separated hexadecimal numbers that follow will be used as i2c addresses. ie "9,0x6b,0x1e"')
    class args():
        def __init__(self):
            parser.parse_args(namespace=self)
            self.DoF = []
            self.getDoF()

        def getDoF(self):
            #set DoF variable
            temp = self.dof.rsplit(',')
            # print(repr(temp))
            for i in range(len(temp)):
                num = int(temp[i], 16)
                if not i:
                    num = int(temp[i])
                    self.DoF.append(num)
                elif not self.is_valid_i2c(num):
                    pass
                else: self.DoF.append(num)

    cmd = args()
    #finish get cmd line args
    if cmd.DoF[0] == 6:
        IMUsensor = MPU6050()
    elif cmd.DoF[0] == 9:
        IMUsensor = LSM9DS1()
    # IMUsensor.set_gyro_range('500')
    while True:
        try:
            print('temp =', IMUsensor.get_temp())
            senses = IMUsensor.get_all_data()
            print('accel =', repr(senses[0]))
            print('gyro =', repr(senses[1]))
            if cmd.DoF[0] == 9:
                print('mag =', repr(senses[2]))
            time.sleep(2)
        except KeyboardInterrupt:
            del IMUsensor
            break
