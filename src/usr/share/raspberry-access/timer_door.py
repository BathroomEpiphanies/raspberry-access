import sqlite3
import time

from door import Door


class TimerDoor(Door):
    
    def __init__(self, database:sqlite3.Cursor) -> None:
        super().__init__(database)
    
    def get_tickets(self, now:float, rfid:str='', pin:str='') -> list[sqlite3.Row]:
        query = f'''
        SELECT
            *
        FROM
            Tickets
        WHERE
            rfid="_timer" AND
            begin<{now} AND end>{now}
        '''
        self.database.execute(query)
        return self.database.fetchall()
    
    def request_access(self, rfid:str='', pin:str='', duration:float=2) -> bool:
        now = time.time()
        tickets = self.get_tickets(now)
        if len(tickets)>0:
            print(f'{time.ctime(now)}, door should be unlocked at this time')
            self.unlock()
            return True
        else:
            print(f'{time.ctime(now)}, door should be locked at this time')
            self.lock()
            return False
    
    def run(self) -> None:
        while True:
            try:
                self.request_access()
                time.sleep(15)
            except KeyboardInterrupt:
                exit(0)
            except:
                import traceback
                traceback.print_exc()
                pass
            finally:
                self.lock()
