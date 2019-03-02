'''
Hardware abstraction layer for communicating with the Arduino.
'''

import serial

# Hardware constants
_speed_max = 2000  # True max: 2000
_speed_min = 700
_speed_range = _speed_max - _speed_min
_baud_rate = 9600

# Serial port is module global
_serial_port = None


def init(port='/dev/ttyACM0'):
    '''
    Initialize the hardware.

    Parameters
    ----------
    port : str
        Port to setup serial for.
    '''
    global _serial_port
    _serial_port = serial.Serial(port, baudrate=_baud_rate)
    #  _serial_port.open()


def cleanup():
    '''
    Shutdown the hardware.
    '''
    global _serial_port
    assert _serial_port
    _serial_port.close()


def set_speeds(speed_left, speed_right):
    '''
    Set left and right motor speeds.

    Parameters
    ----------
    speed_left : float in [0, 1]
        Forward speed of left motor, from stopped to maximum.
    speed_right : float in [0, 1]
        Forward speed of right motor, from stopped to maximum.
    '''
    global _serial_port
    assert _serial_port
    assert _serial_port.is_open
    assert 0 <= speed_left <= 1
    assert 0 <= speed_right <= 1

    speed_left = int((speed_left * _speed_range) + _speed_min)
    speed_right = int((speed_right * _speed_range) + _speed_min)

    serial_string = '{} {}'.format(speed_left, speed_right)
    _serial_port.write(str.encode(serial_string))

    print('Sending string:', serial_string)
