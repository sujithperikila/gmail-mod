import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from search_msg import SearchMessages
from process_msg import ReadMessage
from action import TakeAction
from database import Database
import json
import calendar
import re
import datetime




SCOPES = ['https://mail.google.com/']
our_email = 'perikilasujith@gmail.com'
with open('rules.json','r') as f:
    rules_json = json.load(f)

# Request all access (permission to read/send/receive emails, manage the inbox, and more)


class Main:
    
    def __init__(self):
        self.service = self.gmail_authenticate()
        self.sm = SearchMessages(self.service)
        self.rm = ReadMessage(self.service)
        self.mm = TakeAction(self.service)
        pass
    
    def gmail_authenticate(self):
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)
    
    def get_all_mails(self):
        msgs = self.sm.search_messages('')
        return msgs
        
    
    def get_messages(self):
        msgs = []
        try:
            if rules_json:
                predicate = rules_json['predicate']
                rules_list = rules_json['rules']
                        
            query = ''
            if 'all' in predicate.lower():
                for rule,rule_info in rules_list.items():
                    field = rule_info['field']
                    value = rule_info['value']
                    predicate = rule_info['predicate']
                    if 'from' in field.lower() and 'not' not in predicate:
                        query = query+ f"from:{value} "
                    if 'from' in field.lower() and 'not' in predicate:
                        query = query+ f"from:!{value}"
                        
                        
                    if 'subject' in field.lower() and 'not' not in predicate:
                        query = query+ f"subject:{value} "
                    if 'subject' in field.lower() and 'not' in predicate:
                        query = query+ f"subject:!{value} "
                        
                    if 'date' in field.lower() and ('less' in predicate.lower()):
                        value = int(re.findall(r'\d+', value)[0])
                        query = query+ f"newer_than:{value}d "
                    if 'date' in field.lower() and ('greater' in predicate.lower() or 'more' in predicate.lower()):
                        value = int(re.findall(r'\d+', value)[0])
                        query = query+ f"older_than:{value}d "
                query = query.strip()
                msgs = self.sm.search_messages(query)
            else:
                for rule,rule_info in rules_list.items():
                    field = rule_info['field']
                    value = rule_info['value']
                    predicate = rule_info['predicate']
                    if 'from' in field.lower() and 'not' not in predicate:
                        query = f"from:{value}"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
                    if 'from' in field.lower() and 'not' in predicate:
                        query = f"from:!{value}"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
                        
                        
                    if 'subject' in field.lower() and 'not' not in predicate:
                        query = f"subject:{value}"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
                    if 'subject' in field.lower() and 'not' in predicate:
                        query = f"subject:!{value}"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
                        
                    if 'date' in field.lower() and ('less' in predicate.lower()):
                        value = int(re.findall(r'\d+', value)[0])
                        query = f"newer_than:{value}d"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
                    if 'date' in field.lower() and ('greater' in predicate.lower() or 'more' in predicate.lower()):
                        value = int(re.findall(r'\d+', value)[0])
                        query = f"older_than:{value}d"
                        lst = self.sm.search_messages(query)
                        msgs= list(set(msgs) | set(lst))
        except Exception as e:
            print(e)
            print('Retreiving Messages Failed')
        return msgs
    
    def take_action(self,messages):
        try:
            if 'mark' in rules_json['action'].lower():
                if 'unread' in rules_json['action'].lower():
                    self.mm.mark_as_unread(messages)
                else:
                    self.mm.mark_as_read(messages)
            if 'move' in rules_json['action'].lower():
                pass
            if 'move' in rules_json['action'].lower():
                if 'inbox' in rules_json['action'].lower():
                    self.mm.move_msg(messages,'inbox')
            return True


        except Exception as e:
            print(e)
            print('Action Failed') 
            return False
        
    def filter_messages(self, capped_messages):
        msgs = []
        try:
            if rules_json:
                predicate_ = rules_json['predicate']
                rules_list = rules_json['rules']
                if 'all' in predicate_.lower():
                    for message in capped_messages:
                        c1,c2,c3 = False, False, False
                        for rule,rule_info in rules_list.items():
                            field = rule_info['field']
                            value = rule_info['value']
                            predicate = rule_info['predicate']
                            
                            
                        
                            if 'from' in field.lower():
                                # if not ((( ('not' not in predicate and value in message['from'].lower()))) or ( ('not' in predicate and value not in message['from'].lower()))):
                                #     check = False
                                #     break
                                if 'not' in predicate:
                                    c1 = value not in message['from'].lower()
                                else:
                                    c1 = value in message['from'].lower()
                                
                                
                            if 'subject' in field.lower():
                                # if  (  (not ('not' not in predicate and value in message['subject'].lower()))    or    ( not ('not' in predicate and value not in message['subject'].lower()))):
                                #     check = False
                                #     break
                                if 'not' in predicate:
                                    c2 = value not in message['subject'].lower()
                                else:
                                    c2 = value in message['subject'].lower()
                                    

                            
                            if 'date' in field.lower():
                                if ('less' in predicate.lower()):
                                    today = datetime.date.today()
                                    value = int(value)
                                    c3= (today-message['formatted_date']).days <= value
                                else:
                                    today = datetime.date.today()
                                    value = int(value)
                                    look_from = today+datetime.timedelta(days=value)
                                    c3 = message['formatted_date']<look_from
                                
                        if c1 and c2 and c3:
                            msgs.append(message)
                if 'any' in predicate_.lower():
                    
                    for rule,rule_info in rules_list.items():
                        field = rule_info['field']
                        value = rule_info['value']
                        predicate = rule_info['predicate']
                        for message in capped_messages:
                            check = True
                            
                            if 'from' in field.lower():
                                if ('not' not in predicate and value in message['from']):
                                    if message not in msgs:
                                        msgs.append(message)
                                elif  ('not' in predicate and value not in message['from']):
                                    if message not in msgs:
                                        msgs.append(message)
                                else:
                                    pass
                                
                                
                            if 'subject' in field.lower():
                                if  ('not' not in predicate and value in message['subject']):
                                    if message not in msgs:
                                        msgs.append(message)
                                elif  ('not' in predicate and value not in message['subject']):
                                    if message not in msgs:
                                        msgs.append(message)
                                else:
                                    pass
                                    

                            
                            if 'date' in field.lower():
                                if ('less' in predicate.lower()):
                                    today = datetime.date.today()
                                    value = int(value)
                                    if ((today-message['formatted_date']).days <= value):
                                        if message not in msgs:
                                            msgs.append(message)
                    
                                elif ('greater' in predicate.lower() or 'more' in predicate.lower()):
                                    today = datetime.date.today()
                                    value = int(value)
                                    look_from = today+datetime.timedelta(days=value)
                                    if  message['formatted_date']<look_from:
                                        if message not in msgs:
                                            msgs.append(message)
                                else:
                                    pass
            
    
                        
        except Exception as e:
            print(str(e))
            return []
        return msgs
        
    def format_dates(self, capped_messages):
        for message in capped_messages:
            date = message['date']
            date = date.split(',')[-1].strip().split(' ')[:3]
            day, month, year = int(date[0]), list(calendar.month_abbr).index(date[1]), int(date[2])
            date = datetime.date(year,month, day)
            message['formatted_date'] = date
        return capped_messages

if __name__=='__main__':
    
    from tqdm import tqdm
    import time
    import pickle 
    obj = Main()
    print('Edit values of rules.json file for setting the rules.')
    print('Edit predicate to "all" or "any" as per requiremnet')
    
    
    
    
    s = time.time()
    messages = obj.get_all_mails()
    e = time.time()
    print(f'Time taken to fetch the Emails for Inbox : {e-s} seconds')
    
    
    # capping limit to n number of messages for demo purpose, change the limit value as per your needs.
    limit = 10  # enter a number to set limit,   Enter None if no limit is required( fetches all the mails from gmail account.)
    if limit and len(messages)>limit:
        capped_messages = messages[:limit]
    else:
        capped_messages = messages
        
        
    # procssing messages to add more meta data
    print('Processing Messages')
    for msg in tqdm(range(len(capped_messages))):
        capped_messages[msg] = obj.rm.read_message(capped_messages[msg])
        

    
    # Update Database.   inserting all the mails retreived into the database
    db = Database()
    
    status = db.add_msgs_to_database(capped_messages)
    if status:
        print('Database Update Succesful')
    else:
        print('Database Update Failed / mails already exists in the table')
        
        
    # retreive all the mails stored in the  database ( can be developed into a module, developed a function for assignemtn/demo purpose)
    mails_fetched_from_db = db.get_mails_form_db()
    
    #  convert string date to python's datetime object
    mails_fetched_from_db = obj.format_dates(mails_fetched_from_db)
    
    
    # filter messages as per rules.json
    filtered_msgs = obj.filter_messages(mails_fetched_from_db)
    
    
    # take action on messages as per rules.json
    
    if len(filtered_msgs)>0:
        obj.take_action(filtered_msgs)
        print("Objective Completed")
    else:
        "No Messages retreived based on the filter, therefore,  No action can be taken."
        
        
  


