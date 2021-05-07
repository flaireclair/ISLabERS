import datetime
import sqlite3
from enum import Enum
from gas_connection import GASConnection

class ModeEnum(Enum):
    ENTER = 1
    LEAVE = 2

class DatabaseManager(object):

    def __enter__(self):
        self.conn = sqlite3.connect('idm_list.db')
        self.cur = self.conn.cursor()
        self.dt_now = datetime.datetime.now()
        self.now = self.dt_now.strftime('%Y/%m/%d %a %H:%M')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()

    def subscribe(self, idm, name):
        # print(idm, name, self.now, ModeEnum.LEAVE)
        self.cur.execute('insert into student(idm, name, created_at) values(?,?,?)', (idm,name, self.now))
        self.cur.execute('insert into event(idm, name, mode, accepted_at, created_at) values(?,?,?,?,?)', (idm, name, ModeEnum.LEAVE.value, self.now, self.now))

        print(name + "さん")
        print("登録しました")
        self.conn.commit()

    def update(self, idm):
        data = self.cur.execute('select * from event where idm=?', (idm,))
        data = data.fetchone()

        print(data[1] + "さん")
        print(self.now)

        jdata ={"name" : data[1], "datetime" : str(self.dt_now)}
        if data[2] == ModeEnum.LEAVE.value:
            self.cur.execute('update event set accepted_at=?, mode=? where idm=?', (self.now, ModeEnum.ENTER.value, idm))
            self.cur.execute('insert into record(idm, name, mode, accepted_at) values(?,?,?,?)',(idm, data[1], ModeEnum.ENTER.name, self.now))
            jdata["event"] = ModeEnum.ENTER.name
            is_success = GASConnection().postData(jdata)
            if is_success:
                self.conn.commit()
            else:
                self.conn.rollback()
            print("入室しました")
        else:
            self.cur.execute('update event set accepted_at=?, mode=? where idm=?', (self.now, ModeEnum.LEAVE.value, idm))
            self.cur.execute('insert into record(idm, name, mode, accepted_at) values(?,?,?,?)',(idm, data[1], ModeEnum.LEAVE.name, self.now))
            jdata["event"] = ModeEnum.LEAVE.name
            is_success = GASConnection().postData(jdata)
            if is_success:
                self.conn.commit()
            else:
                self.conn.rollback()
            print("退室しました")
        
