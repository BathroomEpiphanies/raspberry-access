import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


# Door control pins, set both high to activate solid state relay
door_configs = {
    1: {
        'serial_port': '/dev/ttyS0',
        'wiegand_pins': (17,18),
        'output_pins': (22,23),
    },
    2: None,
    3: None,
    4: None,
}

for door_number,door_config in door_configs.items():
    if door_config:
        pin0,pin1 = door_configs[door_number]['output_pins']
        GPIO.setup(pin0,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(pin1,GPIO.OUT,initial=GPIO.LOW)


def unlock_door(door_number,duration):
    pin0,pin1 = door_configs[door_number]['output_pins']
    GPIO.output(pin0,GPIO.HIGH)
    GPIO.output(pin1,GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin0,GPIO.LOW)
    GPIO.output(pin1,GPIO.LOW)




def request_access(door_number=None,database=None,door_name='',rfid='----------',pin='----'):
    now = time.time()
    query = \
        f'SELECT \
              * \
          FROM \
              Tags ta INNER JOIN \
              rTagGroup rtg ON ta.tag_id=rtg.tag_id INNER JOIN \
              Tickets ti ON ti.group_id=rtg.group_id INNER JOIN \
              Doors do ON do.door_id=ti.door_id \
          WHERE \
              do.name="{door_name}" AND \
              ta.rfid="{rfid}" AND \
              ti.begin<"{now}" AND ti.end>"{now}" AND \
              (ta.pin="{pin}" OR ti.require_pin="false")'
    #print(query)
    database.execute(query)

    Tickets = database.fetchall()
    if len(Tickets)>0:
        print(f'time: {time.ctime(now)}, rfid: {rfid}, pin: {pin}, unlocking door for 2 seconds', flush=True)
        unlock_door(door_number=door_number,duration=2)
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
