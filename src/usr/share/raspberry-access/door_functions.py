import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


# System control pins, set all output_pins high to activate solid state relay
system_configurations = {
    "octal": {
        1: {
            'serial_port': '/dev/ttyAMA1',
            'wiegand_pins': (14,15),
            'output_pins':  [2],
        },
        2: {
            'serial_port': None,
            'wiegand_pins': (4,5),
            'output_pins':  [3],
        },
        3: {
            'serial_port': None,
            'wiegand_pins': (22,23),
            'output_pins':  [27],
        },
        4: {
            'serial_port': None,
            'wiegand_pins': (25,10),
            'output_pins':  [24],
        },
        5: {
            'serial_port': None,
            'wiegand_pins': (8,9),
            'output_pins':  [11],
        },
        6: {
            'serial_port': None,
            'wiegand_pins': (12,13),
            'output_pins':  [7],
        },
        7: {
            'serial_port': None,
            'wiegand_pins': (19,16),
            'output_pins':  [6],
        },
        8: {
            'serial_port': None,
            'wiegand_pins': (21,26),
            'output_pins':  [20],
        },
    },
    "quatro": {
        1: {
            'serial_port': '/dev/ttyAMA4',
            'wiegand_pins': (13,12),
            'button_pin':    16,
            'output_pins':  [19],
        },
        2: {
            'serial_port': '/dev/ttyAMA3',
            'wiegand_pins': ( 9, 8),
            'button_pin':    11,
            'output_pins':  [ 7],
        },
        3: {
            'serial_port': '/dev/ttyAMA2',
            'wiegand_pins': ( 5, 4),
            'button_pin':    22,
            'output_pins':  [23],
        },
        4: {
            'serial_port': '/dev/ttyAMA0',
            'wiegand_pins': (15,14),
            'button_pin':    18,
            'output_pins':  [17],
        },
    },
    "single": {
        1: {
            'serial_port': '/dev/ttyAMA0',
            'wiegand_pins': (15,14),
            'button_pin':    11,
            'output_pins':  [6,7],
        },
    },
    "ssr": {
        1: {
            'serial_port': '/dev/ttyS0',
            'wiegand_pins': (17,18),
            'button_pin':     1,
            'output_pins':  [22,23],
        }
    }
}

def setup_relay_pins(system_type,door_number):
    for pin in system_configurations[system_type][door_number]['output_pins']:
        GPIO.setup(pin,GPIO.OUT,initial=GPIO.LOW)


def setup_wiegand_pins(system_type,door_number):
    for pin in system_configurations[system_type][door_number]['wiegand_pins']:
        GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)


def unlock_door(system_type,door_number,duration):
    for pin in system_configurations[system_type][door_number]['output_pins']:
        GPIO.output(pin,GPIO.HIGH)
    time.sleep(duration)
    for pin in system_configurations[system_type][door_number]['output_pins']:
        GPIO.output(pin,GPIO.LOW)




def request_access(system_type=None,door_number=None,database=None,door_name='',rfid='----------',pin='----'):
    now = time.time()
    query = f'''
SELECT
    *
FROM
    Tags ta INNER JOIN
    rUserTag rut ON ta.tag_id=rut.tag_id INNER JOIN
    rUserGroup rug ON rut.user_id=rug.user_id INNER JOIN
    Tickets ti ON ti.group_id=rug.group_id INNER JOIN
    Doors do ON do.door_id=ti.door_id
WHERE
    do.name="{door_name}" AND
    ta.rfid="{rfid}" AND
    ti.begin<{now} AND ti.end>{now} AND
    (ta.pin="{pin}" OR ti.require_pin="false")
'''
    #print(query)
    database.execute(query)
    Tickets = database.fetchall()
    if len(Tickets)>0:
        print(f'time: {time.ctime(now)}, rfid: {rfid}, pin: {pin}, unlocking door for 2 seconds', flush=True)
        unlock_door(system_type,door_number=door_number,duration=2)
        return ('----------','----')
    else:
        print(f'time: {time.ctime(now)}, rfid: {rfid}, pin: {pin}, not unlocking door', flush=True)
        return (rfid,pin)




def raw_to_rfid(raw):
    hej = raw[4:-1]
    hopp = int(hej,16)
    rfid = 0
    rfid += ((hopp >>  2) & 0xF) <<  0
    rfid += ((hopp >>  7) & 0xF) <<  4
    rfid += ((hopp >> 12) & 0xF) <<  8
    rfid += ((hopp >> 17) & 0xF) << 12
    rfid += ((hopp >> 22) & 0xF) << 16
    rfid += ((hopp >> 27) & 0xF) << 20
    rfid += ((hopp >> 32) & 0xF) << 24
    rfid += ((hopp >> 37) & 0xF) << 32
    rfid = '0000000000' + str(rfid)
    return rfid[-10:]
