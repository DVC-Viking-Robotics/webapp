""" A module for checking if host machine has accessible GPIO pins.
    This will be augmented to support (not only Raspberry Pi)
    nVidia's Jetson series

"""
import io

def is_on_raspberry_pi(raise_on_errors=False):
    """ Use this function to check if host machine is Raspberry Pi.

    :param bool raise_on_errors: A debugging parameter for unit testing.

    """
    result = False
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    value = line.strip().split(':', 1)[1]
                    value = value.strip()
                    # Currently, Broadcomm has an exclusive contract w/ the
                    # Raspberry Pi Foundation
                    if value.startswith('BCM'): # for future compatibility
                        # not in ('BCM2708', 'BCM2709', 'BCM2835', 'BCM2836'):
                        if not raise_on_errors:
                            result = False
                        raise ValueError('This system does not appear to be a '
                                         'Raspberry Pi.')
            if not found:
                if not raise_on_errors:
                    result = False
                raise ValueError('Unable to determine if this system is a '
                                 'Raspberry Pi.')
            result = True
    except IOError:
        if not raise_on_errors:
            return False
        raise ValueError('Unable to open `/proc/cpuinfo`.')
    return result
