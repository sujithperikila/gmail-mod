import sqlite3
import datetime


    
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mails.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
            
            return False
        
    def get_mails_form_db(self):
        try:
            msgs = []
            conn = sqlite3.connect('mails.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            cursor = conn.cursor()
            query = '''SELECT * from mails'''
            cursor.execute(query)
            records = cursor.fetchall()
            for item in records:
                tmp={}
                tmp['from'] = item[0]
                tmp['to'] = item[1]
                tmp['subject']  = item[2]
                tmp['date'] = item[3]
                tmp['id'] = item[4]
                tmp['threadId'] = item[5]
                msgs.append(tmp)
            return msgs
        except Exception as e:
            print(str(e))
            return []
        