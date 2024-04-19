#!/usr/bin/python3 -u

import argparse
import sys
import time
import RPi.GPIO as GPIO
import sqlite3

from door_functions import system_configurations


def has_access(database, door_name):
    now = time.time()
    group_name = '_timer'
    door_id = database.execute(f'SELECT door_id FROM Doors WHERE name="{door_name}"').fetchone()[0]
    group_id = database.execute(f'SELECT group_id FROM Groups WHERE name="{group_name}"').fetchone()[0]
    tickets = database.execute(f'SELECT * FROM Tickets WHERE door_id={door_id} AND group_id={group_id} AND begin<{now} AND end>{now}').fetchall()
    return len(tickets)>0


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
                        help     = 'Physical door number [1,2,3,4,...].')
    args = parser.parse_args()
    
    database = sqlite3.connect(args.database, check_same_thread=False).cursor()
    door_name = args.door_name
    system_type = args.system_type
    door_number = args.door_number
    
    relay_pin = system_configurations[system_type][door_number]['output_pins'][0]
    GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)
    
    print(f'Starting: {time.ctime()}', file=sys.stderr, flush=True)
    while True:
        try:
            time.sleep(15)
            if has_access(database, door_name):
                GPIO.output(relay_pin, GPIO.HIGH)
                print(f'{door_name} should be unlocked at this time {time.time()}', file=sys.stderr, flush=True)
            else:
                GPIO.output(relay_pin, GPIO.LOW)
                print(f'{door_name} should be locked at this time {time.time()}', file=sys.stderr, flush=True)
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit(0)
        except:
            import traceback
            traceback.print_exc(file=sys.stderr)
            pass

if __name__ == '__main__':
    main()
