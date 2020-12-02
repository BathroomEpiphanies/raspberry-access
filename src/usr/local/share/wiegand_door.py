#!/usr/bin/python3 -u

import argparse
import serial
import sys
import time
import RPi.GPIO as GPIO
import sqlite3

from door_functions import request_access


# Wiegand input pins
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# First and last bits are parity checks
# mask them off and hope there are no errors...
#
#         1000010010101011110100000101101001
bitmask  = 0b0111111111111111111111111111111110
bitcount = 0
timestamp = 0
state = 0
def wiegand(pin):
    global bitcount
    global state
    global timestamp
    global database
    global door_number
    global door_name
    t = time.time()
    if t > timestamp + 0.005:
        state = (0 if pin==17 else 1)
        bitcount = 1
    else:
        state = state*2 + (0 if pin==17 else 1)
        bitcount += 1
    timestamp = t
    if bitcount >= 34:
        rfid = f'{(state&bitmask)>>1:010d}'
        request_access(door_number=door_number,database=database,door_name=door_name,rfid=rfid,pin='')



database = None
door_number = None
door_name = None
def main():
    global database
    global door_number
    global door_name
    
    parser = argparse.ArgumentParser(description='Door access system.')
    parser.add_argument('--database',
                        required = True,
                        help     = 'Database file [/perm/database.sqlite].')
    parser.add_argument('--door-name',
                        required = True,
                        help     = 'Door identifier [door-djurhuset,door-prototype,..].')
    parser.add_argument('--door-number',
                        required = True,
                        type     = int,
                        help     = 'Physical door controller number [1,2,3,4].')
    args = parser.parse_args()
    
    database = sqlite3.connect(args.database,check_same_thread=False).cursor()
    door_number = args.door_number
    door_name = args.door_name
    
    print(f'Starting: {time.ctime()}',flush=True)
    GPIO.add_event_detect(17,GPIO.FALLING,callback=wiegand,bouncetime=1)
    GPIO.add_event_detect(18,GPIO.FALLING,callback=wiegand,bouncetime=1)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit(0)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout,flush=True)
            pass

if __name__ == '__main__':
    main()
