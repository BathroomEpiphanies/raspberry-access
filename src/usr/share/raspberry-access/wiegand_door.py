import signal
import sqlite3
import time
from collections import deque

import RPi.GPIO as GPIO

from door import Door
from hardware import WiegandPins


class WiegandDoor(Door):
    
    wiegand_pins:WiegandPins
    wiegand_stream:deque[int]
    timestamp:float
    
    def __init__(self, connection:sqlite3.Cursor) -> None:
        super().__init__(connection)
        self.wiegand_pins = self.hardware[self.port].wiegand_pins
        self.wiegand_stream = deque(maxlen=34)
        self.timestamp = 0
        GPIO.setup(self.wiegand_pins.w0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.wiegand_pins.w1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.wiegand_pins.w0, GPIO.FALLING, callback=self.interrupt_callback, bouncetime=1)
        GPIO.add_event_detect(self.wiegand_pins.w1, GPIO.FALLING, callback=self.interrupt_callback, bouncetime=1)
    
    def interrupt_callback(self, pin:int) -> None:
        now = time.time()
        if now>self.timestamp+0.1:
            self.wiegand_stream.clear()
        self.timestamp = now
        self.wiegand_stream.append(0 if pin==self.wiegand_pins.w0 else 1)
        rfid = self.check_rfid()
        if rfid and self.request_access(rfid, pin='', duration=2) and time.sleep(2):
            self.wiegand_stream.clear()
    
    def check_rfid(self) -> str:
        stream = list(self.wiegand_stream)
        length = len(stream)
        parity1 = sum(stream[:17])%2
        parity2 = sum(stream[17:])%2
        if length==34 and parity1==0 and parity2==1:
            rfid = sum(d*2**p for p,d in enumerate(reversed(stream[1:-1])))
            return f'{rfid:010d}'
        else:
            return ''
    
    def run(self) -> None:
        super().run()
        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                exit(0)
            except:
                import traceback
                traceback.print_exc()
                pass
            finally:
                self.lock()
