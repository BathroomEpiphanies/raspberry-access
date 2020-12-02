#!/usr/bin/python3 -u

import argparse
import serial
import sys
import time
import RPi.GPIO as GPIO
import sqlite3

from door_functions import request_access,door_configs,raw_to_rfid


def main():
    parser = argparse.ArgumentParser(description='Door access system.')
    parser.add_argument('--database',
                        required = True,
                        help     = 'Database file.')
    parser.add_argument('--door-name',
                        required = True,
                        help     = 'Door identifier.')
    parser.add_argument('--door-number',
                        required = True,
                        type     = int,
                        help     = 'Physical door controller number [1,2,3,4].')
    args = parser.parse_args()
    
    database = sqlite3.connect(args.database,check_same_thread=False).cursor()
    
    rfid,pin = request_access(args.door_number,database)
    
    print(f'Starting: {time.ctime()}',flush=True)
    while True:
        try:
            UART = serial.Serial(door_configs[args.door_number]['serial_port'],9600)
            UART.close()
            UART.open()
            while True:
                c = UART.read(1)
                if c and ord(c) == 0x11:
                    rfid = raw_to_rfid(UART.read(16).decode('utf-8'))
                elif c and ord(c) == 0x12:
                    pin = pin[-3:] + UART.read(1).decode('utf-8')
                rfid,pin = request_access(args.door_number,database,args.door_name,rfid,pin)
                    
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout,flush=True)
            pass

if __name__ == '__main__':
    main()
