
from search_msg import SearchMessages

class TakeAction:
    def __init__(self,service):
        self.service = service
        self.sm = SearchMessages(self.service)
        pass

    def mark_as_read(self, messages_to_mark):
        # messages_to_mark = self.sm.search_messages(self.service, query)
        print(f"Marking as Read {len(messages_to_mark)} filtered emails")
        return self.service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'removeLabelIds': ['UNREAD']
        }
        ).execute()
    

    def mark_as_unread(self, messages_to_mark):
        # messages_to_mark = self.sm.search_messages(self.service, query)
        print(f"Marking as UnRead {len(messages_to_mark)} filtered emails")
        # add the label UNREAD to each of the search results
        return self.service.users().messages().batchModify(
            userId='me',
            body={
                'ids': [ msg['id'] for msg in messages_to_mark ],
                'addLabelIds': ['UNREAD']
            }
        ).execute()
        
    def move_msg(self,messages_to_mark,dest):
        if 'inbox' in dest:
            return self.service.users().messages().batchModify(
            userId='me',
            body={
                'ids': [ msg['id'] for msg in messages_to_mark ],
                'addLabelIds': ['INBOX']
            }
            ).execute()