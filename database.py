import sqlite3
import datetime


    
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mails.db')
        if self.conn:
            "Database Initiated Successfully"
    
    def create_table(self):
        try:
            self.conn.execute('''CREATE TABLE mails (from_mail TEXT NOT NULL,to_mail TEXT NOT NULL,subject TEXT NOT NULL,date TEXT NOT NULL,id TEXT PRIMARY KEY NOT NULL,  thread_id CHAR(100) NOT NULL);''')
        except Exception as e:
            print(str(e))
    
    def add_msgs_to_database(self,msgs):
        self.create_table()
        try:
            now = datetime.datetime.now()
            tid = now.strftime("%Y-%m-%d %H:%M:%S")
            tid = int(tid.replace(':','').replace(' ','').replace('-',''))
            for msg in msgs:
                self.conn.execute('''INSERT INTO mails (from_mail,to_mail,subject,date,id,thread_id) VALUES(?,?,?,?,?,?);''',(msg['from'],msg['to'],msg['subject'],msg['date'],msg['id'], msg['threadId']))
            self.conn.commit()
            print("Records created successfully")
            self.conn.close()
            return True
        except Exception as e:
            print(str(e))
            return False