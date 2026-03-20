#!/usr/bin/python3 -u

import argparse
import sqlite3

from door import Door
from timer_door import TimerDoor
from uart_door import UARTDoor
from wiegand_door import WiegandDoor


def main() -> None:
    parser = argparse.ArgumentParser(description='Door access system.')
    parser.add_argument('--database',
                        required = True,
                        help     = 'Database file.')
    args = parser.parse_args()
    
    database:sqlite3.Cursor = sqlite3.connect(args.database, check_same_thread=False).cursor()
    database.row_factory = sqlite3.Row
    door_data:dict[str,str] = database.execute('SELECT * FROM Metadata').fetchone()
    door_type:str = door_data['reader_type']
    door:Door
    match door_type:
        case 'timer':
            door = TimerDoor(database)
        case 'uart':
            door = UARTDoor(database)
        case 'wiegand':
            door = WiegandDoor(database)
    door.run()


if __name__ == '__main__':
    main()
