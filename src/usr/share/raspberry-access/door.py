from typing import Any

import sqlite3
import time
from abc import ABC, abstractmethod

import RPi.GPIO as GPIO

from hardware import hardware_variants


class Door(ABC):
    
    database:sqlite3.Cursor
    name:str
    port:int
    solenoid_pins:list[int]
    
    def __init__(self, database:sqlite3.Cursor) -> None:
        super().__init__()
        self.database = database
        door_data = self.database.execute('SELECT * FROM Metadata').fetchone()
        self.name = door_data['name']
        self.hardware = hardware_variants[door_data['hardware']]
        self.port = door_data['hardware_port']
        
        self.solenoid_pins = self.hardware[self.port].solenoid_pins
        for solenoid_pin in self.solenoid_pins:
            GPIO.setup(solenoid_pin, GPIO.OUT, initial=GPIO.LOW)

    def unlock(self) -> None:
        for solenoid_pin in self.solenoid_pins:
            GPIO.output(solenoid_pin, GPIO.HIGH)
    
    def lock(self) -> None:
        for solenoid_pin in self.solenoid_pins:
            GPIO.output(solenoid_pin, GPIO.LOW)
    
    def get_tickets(self, now:float, rfid:str, pin:str) -> list[sqlite3.Row]:
        query = f'''
        SELECT 
            *
        FROM
            Tickets WHERE rfid="{rfid}" AND 
            begin<{now} AND end>{now} AND 
            (pin="{pin}" OR require_pin="false")
        '''
        self.database.execute(query)
        return self.database.fetchall()
    
    def request_access(self, rfid:str, pin:str, duration:int=2) -> bool:
        now = time.time()
        tickets = self.get_tickets(now, rfid, pin)
        if len(tickets)>0:
            print(f'{time.ctime(now)}, {rfid=}, {pin=}, unlocking door for {duration} seconds')
            self.unlock()
            time.sleep(duration)
            self.lock()
            return True
        else:
            print(f'{time.ctime(now)}, {rfid=}, {pin=}, not unlocking door')
            return False
    
    @abstractmethod
    def run(self) -> None:
        print(f'Starting: {time.ctime()}')
