import sqlite3
import datetime


    
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mails.db')
        if self.conn:
            "Database Initiated Successfully"
    
    def create_table(self):
        try:
            self.conn.execute('''CREATE TABLE mails (id TEXT PRIMARY KEY NOT NULL, tid INT NOT NULL ,  thread_id CHAR(100) NOT NULL);''')
        except Exception as e:
            print(str(e))
    
    def add_msgs_to_database(self,msgs):
        self.create_table()
        try:
            now = datetime.datetime.now()
            tid = now.strftime("%Y-%m-%d %H:%M:%S")
            tid = int(tid.replace(':','').replace(' ','').replace('-',''))
            for msg in msgs:
                self.conn.execute('''INSERT INTO mails (id,tid,thread_id) VALUES(?,?,?);''',(msg['id'], tid, msg['threadId']))
            self.conn.commit()
            print("Records created successfully")
            self.conn.close()
            return True
        except Exception as e:
            print(str(e))
            return False