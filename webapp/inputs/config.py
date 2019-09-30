# pylint: disable=anomalous-backslash-in-string,missing-docstring,invalid-name,relative-beyond-top-level
import json
try:
    import board
except NotImplementedError:
    pass  # addressed by has_gpio_pins variable
from gps_serial import GPSserial
from .check_platform import ON_RASPI, ON_JETSON

if ON_RASPI:
    from drivetrain.drivetrain import Tank, Automotive, External
    from drivetrain.motor import Solenoid, BiMotor, PhasedMotor, NRF24L01, USB
    from adafruit_lsm9ds1 import LSM9DS1_I2C
    from circuitpython_mpu6050 import MPU6050

from .imu import MAG3110

CONFIG_FILE_LOCATION = u'webapp/inputs/HWconfig.json'
SYSTEM_CONF = None

try:
    with open(CONFIG_FILE_LOCATION, 'r') as conf_file:
        SYSTEM_CONF = json.load(conf_file)
except FileNotFoundError:
    print(f'Unable to find config file @ {CONFIG_FILE_LOCATION}. Skipping hardware check...')

has_gpio_pins = ON_RASPI or ON_JETSON

if has_gpio_pins:
    SPI_BUS = board.SPI()
    I2C_BUS = board.I2C()
    RPI_PIN_ALIAS = {
        '2': board.D2,
        '3': board.D3,
        '4': board.D4,
        '5': board.D5,
        '6': board.D6,
        '7': board.D7,
        '8': board.D8,
        '9': board.D9,
        '10': board.D10,
        '11': board.D11,
        '12': board.D12,
        '13': board.D13,
        '14': board.D14,
        '15': board.D15,
        '16': board.D16,
        '17': board.D17,
        '18': board.D18,
        '19': board.D19,
        '20': board.D20,
        '21': board.D21,
        '22': board.D22,
        '23': board.D23,
        '24': board.D24,
        '25': board.D25,
        '26': board.D26,
        '27': board.D27,
    }

d_train = []
IMUs = []
gps = []
nav = None

if SYSTEM_CONF is not None:
    if 'Drivetrains' in SYSTEM_CONF['Check-Hardware']:
        # handle drivetrain
        for d in SYSTEM_CONF['Drivetrains']:
            if d['type'] in ('Tank', 'Automotive', 'External'):
                # instantiate motors
                motors = []
                for m in d['motors']:
                    # detirmine driver class
                    pins = []
                    # be sure its not a serial port address
                    if m['address'].find(',') > 0 and has_gpio_pins:
                        for p in m['address'].rsplit(','):
                            pins.append(RPI_PIN_ALIAS[p])
                    if m['driver'].startswith('Solenoid') and len(pins) >= 1 and has_gpio_pins:
                        motors.append(Solenoid(pins))
                    elif m['driver'].startswith('BiMotor') and len(pins) >= 1 and has_gpio_pins:
                        motors.append(BiMotor(pins))
                    elif m['driver'].startswith('PhasedMotor') and len(pins) == 2 and has_gpio_pins:
                        motors.append(PhasedMotor(pins))
                    elif m['driver'].startswith('NRF24L01') and has_gpio_pins:
                        motors.append(
                            NRF24L01(SPI_BUS, pins, bytes(m['name'].encode('utf-8'))))
                    elif m['driver'].startswith('USB'):
                        motors.append(USB(m['address']))
                if d['type'].startswith('Tank') and has_gpio_pins:
                    d_train.append(Tank(motors, int(d['max speed'])))
                elif d['type'].startswith('Automotive') and has_gpio_pins:
                    d_train.append(Automotive(motors, int(d['max speed'])))
                elif d['type'].startswith('External'):
                    if motors:
                        d_train.append(External(motors[0]))

    if 'IMU' in SYSTEM_CONF['Check-Hardware']:
        for imu in SYSTEM_CONF['IMU']:
            pins = []
            # be sure its not a serial port address
            if imu['address'].find(',') > 0 and has_gpio_pins:
                for p in imu['address'].rsplit(','):
                    pins.append(int(p, 16))
            if imu['driver'].startswith('LSM9DS1') and has_gpio_pins:
                IMUs.append(LSM9DS1_I2C(I2C_BUS, pins[0], pins[1]))
            elif imu['driver'].startswith('MPU6050') and has_gpio_pins:
                IMUs.append(MPU6050(I2C_BUS))
            elif imu['driver'].startswith('MAG3110'):
                IMUs.append(MAG3110(imu['address']))

    if 'GPS' in SYSTEM_CONF['Check-Hardware']:
        for g in SYSTEM_CONF['GPS']:
            if g['driver'].startswith('GPSserial'):
                gps.append(GPSserial(g['address']))

    if gps and IMUs and d_train:
        from ..outputs.GPSnav import GPSnav
        nav = GPSnav(d_train[0], IMUs, gps)
