#!/usr/bin/python3 -u

import argparse
import serial
import sys
import time
import RPi.GPIO as GPIO
import sqlite3

from door_functions import system_configurations,request_access,setup_relay_pins,setup_wiegand_pins,raw_to_rfid


def main():
    parser = argparse.ArgumentParser(description='Door access system.')
    parser.add_argument('--database',
                        required = True,
                        help     = 'Database file [/perm/database.sqlite].')
    parser.add_argument('--door-name',
                        required = True,
                        help     = 'Computer identifier [door-djurhuset,door-prototype,..].')
    parser.add_argument('--system-type',
                        required = True,
                        help     = 'Circuit board type [ssr,quatro,..].')
    parser.add_argument('--door-number',
                        required = True,
                        type     = int,
                        help     = 'Physical door number [1,2,3,4].')
    args = parser.parse_args()
    
    database = sqlite3.connect(args.database,check_same_thread=False).cursor()
    door_number = args.door_number
    door_name = args.door_name
    system_type = args.system_type
    
    setup_relay_pins(system_type,door_number)
    UART = serial.Serial(system_configurations[system_type][door_number]['serial_port'],9600)
    rfid,pin = request_access(system_type,door_number,database)
    
    print(f'Starting: {time.ctime()}',flush=True)
    while True:
        try:
            UART.close()
            UART.open()
            while True:
                c = UART.read(1)
                if c and ord(c) == 0x11:
                    rfid = raw_to_rfid(UART.read(16).decode('utf-8'))
                elif c and ord(c) == 0x12:
                    pin = pin[-3:] + UART.read(1).decode('utf-8')
                rfid,pin = request_access(system_type,door_number,database,door_name,rfid,pin)
        
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout,flush=True)
            pass

if __name__ == '__main__':
    main()
