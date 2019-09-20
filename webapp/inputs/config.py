# pylint: disable=anomalous-backslash-in-string,missing-docstring,invalid-name
import json
try:
    import board
except NotImplementedError:
    pass # addressed by has_gpio_pins variable
from circuitpython_mpu6050 import MPU6050
from .check_platform import is_on_raspberry_pi
from ..Drivetrain.drivetrain.motor import Solonoid, BiMotor, PhasedMotor, NRF24L01, USB
from ..Drivetrain.drivetrain.drivetrain import BiPed, QuadPed, External
from ..inputs.imu import LSM9DS1_I2c, MAG3110
from ..GPS_Serial.gps_serial import GPSserial

with open(u'webapp\inputs\config.json', 'r') as conf_file:
    SYSTEM_CONF = json.load(conf_file)

has_gpio_pins = is_on_raspberry_pi()
if has_gpio_pins:
    SPI_BUS = board.SPI()
    I2C_BUS = board.I2C()
    RPI_PIN_ALIAS = {
        '10':board.D10,
        '11':board.D11,
        '12':board.D12,
        '13':board.D13,
        '14':board.D14,
        '15':board.D15,
        '16':board.D16,
        '17':board.D17,
        '18':board.D18,
        '19':board.D19,
        '2':board.D2,
        '20':board.D20,
        '21':board.D21,
        '22':board.D22,
        '23':board.D23,
        '24':board.D24,
        '25':board.D25,
        '26':board.D26,
        '27':board.D27,
        '3':board.D3,
        '4':board.D4,
        '5':board.D5,
        '6':board.D6,
        '7':board.D7,
        '8':board.D8,
        '9':board.D9,
    }

d_train = []

# handle drivetrain
for d in SYSTEM_CONF['Drivetrains']:
    if d['type'] in ('BiPed', 'QuadPed', 'External'):
        # instantiate motors
        motors = []
        for m in d['motors']:
            # detirmine driver class
            pins = []
            if m['address'].find(',') > 0 and has_gpio_pins: # be sure its not a serial port address
                for p in m['address'].rsplit(','):
                    pins.append(RPI_PIN_ALIAS[p])
            if m['driver'].startswith('Solonoid') and len(pins) >= 1 and has_gpio_pins:
                motors.append(Solonoid(pins))
            elif m['driver'].startswith('BiMotor') and len(pins) >= 1 and has_gpio_pins:
                motors.append(BiMotor(pins))
            elif m['driver'].startswith('PhasedMotor') and len(pins) == 2 and has_gpio_pins:
                motors.append(PhasedMotor(pins))
            elif m['driver'].startswith('NRF24L01') and has_gpio_pins:
                motors.append(NRF24L01(SPI_BUS, pins, bytes(m['name'].encode('utf-8'))))
            elif m['driver'].startswith('USB'):
                motors.append(USB(m['address']))
        if d['type'].startswith('BiPed') and has_gpio_pins:
            d_train.append(BiPed(motors, d['max speed']))
        elif d['type'].startswith('QuadPed') and has_gpio_pins:
            d_train.append(QuadPed(motors, d['max speed']))
        elif d['type'].startswith('External'):
            if motors:
                d_train.append(External(motors[0]))


IMUs = []
for imu in SYSTEM_CONF['IMU']:
    pins = []
    if imu['address'].find(',') > 0 and has_gpio_pins: # be sure its not a serial port address
        for p in imu['address'].rsplit(','):
            pins.append(int(p, 16))
    if imu['driver'].startswith('LSM9DS1') and has_gpio_pins:
        IMUs.append(LSM9DS1_I2c(I2C_BUS, pins[0], pins[1]))
    elif imu['driver'].startswith('MPU6050') and has_gpio_pins:
        IMUs.append(MPU6050(I2C_BUS))
    elif imu['driver'].startswith('MAG3110'):
        IMUs.append(MAG3110(imu['address']))

if SYSTEM_CONF['GPS']['interface'].startswith('serial'):
    gps = GPSserial(SYSTEM_CONF['GPS']['address'])
else: gps = None

if gps is not None and IMUs and d_train:
    from ..outputs.GPSnav import GPSnav
    nav = GPSnav(d_train[0], IMUs, gps)
else: nav = None
