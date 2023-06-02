import os
from base64 import urlsafe_b64decode



class ReadMessage:
    def __init__(self,service):
        self.service = service
        pass
    
    
    def read_message(self, message):
        """
        This function takes Gmail API `self.service` and the given `message_id` and does the following:
            - Downloads the content of the email
            - Prints email basic information (To, From, Subject & Date) and plain/text parts
            - Creates a folder for each email based on the subject
            - Downloads text/html content (if available) and saves it under the folder created as index.html
            - Downloads any file that is attached to the email and saves it in the folder created
        """
        msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # parts can be the message body, or attachments
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        folder_name = "email"
        has_subject = False
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    # print("From:", value)
                    message['from'] = value
                if name.lower() == "to":
                    # we print the To address
                    # print("To:", value)
                    message['to'] = value
                if name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    has_subject = True
                    # make a directory with the name of the subject
                    folder_name = self.clean(value)
                    # we will also handle emails with the same subject name
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    # os.mkdir(folder_name)
                    # print("Subject:", value)
                    message['subject'] = value
                if name.lower() == "date":
                    # we print the date when the message was sent
                    # print("Date:", value)
                    message['date'] = value
        if not has_subject:
            # if the email does not have a subject, then make a folder with "email" name
            # since folders are created based on subjects
            # if not os.path.isdir(folder_name):
            #     os.mkdir(folder_name)
            message['subject'] = 'no subject'
        # self.parse_parts(self.service, parts, folder_name, message)
        return message
        # print("="*50)

    def get_size_format(self,b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


    def clean(self,text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    