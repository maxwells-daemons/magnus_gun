'''
Hardware abstraction layer for communicating with the Arduino.
'''

import time
import serial
import numpy as np

# Hardware constants
_speed_max = 2000  # True max: 2000
_speed_min = 700
_speed_range = _speed_max - _speed_min
_baud_rate = 9600

# Module globals
_serial_port = None
_setpoint_left = None
_setpoint_right = None


def init(port='/dev/ttyACM1'):
    '''
    Initialize the hardware.

    Parameters
    ----------
    port : str
        Port to setup serial for.
    '''
    global _serial_port
    _serial_port = serial.Serial(port, baudrate=_baud_rate)


def calibrate():
    '''
    Calibrate the hardware.
    '''
    set_speeds(_speed_max, _speed_max)
    time.sleep(5)
    set_speeds(_speed_min, _speed_min)
    time.sleep(3)
    set_speeds(1000, 1000)
    time.sleep(1)
    set_speeds(_speed_min, _speed_min)


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
    speed_left : int in [700, 2000]
        Forward speed of left motor, from stopped to maximum.
    speed_right : int in [700, 2000]
        Forward speed of right motor, from stopped to maximum.
    '''
    global _serial_port
    global _setpoint_left
    global _setpoint_right

    assert _serial_port
    assert _serial_port.is_open
    assert _speed_min <= speed_left <= _speed_max
    assert _speed_min <= speed_right <= _speed_max

    if (speed_left == _setpoint_left and speed_right == _setpoint_right):
        return

    _setpoint_left = speed_left
    _setpoint_right = speed_right

    serial_string = '{} {}\n'.format(speed_left, speed_right)
    _serial_port.write(str.encode(serial_string))

    print('Sending string:', serial_string)


def set_speeds_ramp(speed_left, speed_right, ramp_rate=200, pt_per_sec=10):
    '''
    Set left and right motor speeds, ramping from the current value.

    Parameters
    ----------
    speed_left : int in [700, 2000]
        Forward speed of left motor, from stopped to maximum.
    speed_right : int in [700, 2000]
        Forward speed of right motor, from stopped to maximum.
    ramp_rate : int
        Microseconds per second to ramp by.
    pts_per_sec : int
        Number of interpolation points traversed per second.
    '''
    if speed_left < _setpoint_left and speed_right < _setpoint_right:
        set_speeds(speed_left, speed_right)
        return

    vals_left = np.arange(_setpoint_left, speed_left, ramp_rate / pt_per_sec)
    vals_right = np.arange(_setpoint_right, speed_left, ramp_rate / pt_per_sec)
    delay_per_tick = 1. / pt_per_sec

    for new_speed_left, new_speed_right in zip(vals_left, vals_right):
        set_speeds(new_speed_left, new_speed_right)
        time.sleep(delay_per_tick)
