import binascii
import nfc
import datetime
import sqlite3
import time
from database_manager import DatabaseManager
from card_reader import CardReader

if __name__ == '__main__':
    cr = CardReader()

    while True:
        new_idm = ""
        print() 
        cr.read_idm()
        if(cr.idm != ""):
            new_idm = str(cr.idm)
            new_idm = new_idm[2:-1]

            with DatabaseManager() as dm:
                dm.update(new_idm)
            time.sleep(1)
        else:
            print()
            break
