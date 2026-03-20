from typing import NamedTuple

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)


class WiegandPins(NamedTuple):
    w0:int
    w1:int


class HardwarePort(NamedTuple):
    serial_port:str|None
    wiegand_pins:WiegandPins
    solenoid_pins:list[int]


hardware_variants = {
    "octal_20260223": {
        1: HardwarePort('/dev/serial0', WiegandPins(14,15), [17]),
        2: HardwarePort('/dev/serial1', WiegandPins( 4, 5), [18]),
        3: HardwarePort(          None, WiegandPins(22,23), [27]),
        4: HardwarePort(          None, WiegandPins(15,10), [24]),
        5: HardwarePort('/dev/serial2', WiegandPins( 8, 9), [11]),
        6: HardwarePort(          None, WiegandPins( 7, 6), [19]),
        7: HardwarePort('/dev/serial3', WiegandPins(12,13), [16]),
        8: HardwarePort(          None, WiegandPins(26,21), [20]),
    },
    "octal_20230814": {
        1: HardwarePort('/dev/serial0', WiegandPins(14,15), [ 2]),
        2: HardwarePort('/dev/serial1', WiegandPins( 4, 5), [ 3]),
        3: HardwarePort('/dev/serial2', WiegandPins(22,23), [27]),
        4: HardwarePort('/dev/serial3', WiegandPins(25,10), [24]),
        5: HardwarePort(          None, WiegandPins( 8, 9), [11]),
        6: HardwarePort(          None, WiegandPins(12,13), [ 7]),
        7: HardwarePort(          None, WiegandPins(19,16), [ 6]),
        8: HardwarePort(          None, WiegandPins(21,26), [20]),
    },
    "quatro": {
        1: HardwarePort('/dev/ttyAMA4', WiegandPins(13,12), [19]),
        2: HardwarePort('/dev/ttyAMA3', WiegandPins( 9, 8), [ 7]),
        3: HardwarePort('/dev/ttyAMA2', WiegandPins( 5, 4), [23]),
        4: HardwarePort('/dev/ttyAMA0', WiegandPins(15,14), [17]),
    },
    "single": {
        1: HardwarePort('/dev/serial0', WiegandPins(13,12), [17]),
    },
    "ssr": {
        1: HardwarePort('/dev/ttyS0', WiegandPins(17,18), [22,23]),
    },
}
