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
import re





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
        
        
        

if __name__=='__main__':
    
    
    obj = Main()
    print('Edit values of rules.json file for setting the rules.')
    print('Edit predicate to "all" or "any" as per requiremnet')
    
#      "predicate" : "all" or "any"

#      "rules" format
#      "field_name":["From","Subject","Date Received"],
#      "predicate":["contains","does not contains","less than","greater than"],
#      "value":[] -> anything as per requiremenet


#      "action" : "mark as read" or "mark as unread" or "move message"
    messages = obj.get_messages()
    # take action on messages
    if len(messages)>0:
        obj.take_action(messages)
    else:
        "No Messages retreived based on the filter, therefore,  No action can be taken."
        
        
    # Update Database
    db = Database()
    for msg in range(len(messages)):
        messages[msg] = obj.rm.read_message(messages[msg])
    status = db.add_msgs_to_database(messages)
    if status:
        print('Database Update Succesful')
    else:
        print('Database Update Failed')


    print("Objective Completed")