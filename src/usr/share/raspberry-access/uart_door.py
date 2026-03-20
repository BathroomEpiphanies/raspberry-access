import serial
import sqlite3
import traceback
from collections import deque


from door import Door


class UARTDoor(Door):
    
    serial_port:str
    UART:serial.serialposix.Serial
    raw:deque[str]
    pin:deque[str]
        
    def __init__(self, database:sqlite3.Cursor) -> None:
        super().__init__(database)
        
        serial_port = self.hardware[self.port].serial_port
        if not isinstance(serial_port, str):
            raise RuntimeError(f'Port {self.port} is not connected to serial interface')
        self.serial_port = serial_port
        self.UART = serial.Serial(self.serial_port, 9600)
        self.raw = deque(maxlen=16)
        self.pin = deque(maxlen=4)
    
    def run(self) -> None:
        super().run()
        while True:
            try:
                self.UART.close()
                self.UART.open()
                while True:
                    char = self.UART.read(1)
                    if char and ord(char) == 0x11:
                        self.raw.extend(self.UART.read(16).decode('utf-8'))
                    elif char and ord(char) == 0x12:
                        self.pin.extend(self.UART.read(1).decode('utf-8'))
                    self.UART.read(1)
                    raw = ''.join(self.raw)
                    rfid = raw_to_rfid(raw)
                    pin = ''.join(self.pin)
                    if self.request_access(rfid, pin, duration=2):
                        self.raw.clear()
                        self.pin.clear()
            except KeyboardInterrupt:
                exit(0)
            except:
                traceback.print_exc()
                pass
            finally:
                self.lock()


def raw_to_rfid(raw:str) -> str:
    try:
        raw_ = int(raw, 16)
        rfid = 0
        rfid += (raw_ & 0b000000000_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_1111_0_0000_0) >>  6
        rfid += (raw_ & 0b000000000_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_1111_0_0000_0_0000_0) >>  7
        rfid += (raw_ & 0b000000000_0000_0_0000_0_0000_0_0000_0_0000_0_1111_0_0000_0_0000_0_0000_0) >>  8
        rfid += (raw_ & 0b000000000_0000_0_0000_0_0000_0_0000_0_1111_0_0000_0_0000_0_0000_0_0000_0) >>  9
        rfid += (raw_ & 0b000000000_0000_0_0000_0_0000_0_1111_0_0000_0_0000_0_0000_0_0000_0_0000_0) >> 10
        rfid += (raw_ & 0b000000000_0000_0_0000_0_1111_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0) >> 11
        rfid += (raw_ & 0b000000000_0000_0_1111_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0) >> 12
        rfid += (raw_ & 0b000000000_1111_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0_0000_0) >> 13
        return f'{rfid:010d}'
    except ValueError:
        return ''
