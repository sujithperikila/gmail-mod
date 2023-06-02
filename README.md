
# HappyFox Assignment
# By Sujith Perikila

Problem Statement : Write Python scripts that integrates with GMail API and performs some rule based
operations on emails.

# Install Requirements
    pip3 install -r requirements.txt

# Enable GMAIL API
1.To use the Gmail API, we need a token to connect to Gmail's API. We can get one from the Google APIs' dashboard.
We first enable the Google mail API, head to the dashboard, and use the search bar to search for Gmail API, click on it, and then enable.

2.We then create an OAuth 2.0 client ID by creating credentials (by heading to the Create Credentials button)

3.Click on Create Credentials, and then choose OAuth client ID from the dropdown menu.

4.You'll be headed to 'Create OAuth client ID page. Select Desktop App as the Application type and proceed.

5.Go ahead and click on DOWNLOAD JSON; it will download a long-named JSON file. Rename it to 'credentials.json' and put it in the current directory of the project.

# File Modifications
main.py

    main.py, line 19, 
    change 'our_email' variable value to your email.
rules.json

    change rules.json rules as per requirement.

# Rules Modifications
     "predicate" : "all" or "any" 

     "rules" format : 
     "field_name":["From","Subject","Date Received"],   
     "predicate":["contains","does not contains","less than","greater than"],
     "value":[] -> value to be matched as per requiremenet
     "action" : "mark as read" or "mark as unread" or "move message to inbox"

# Running main.py
After all the required Modifications as done, run the main script by executing the below command
    
    python3 main.py 
You might be asked to authenticate via Google page, post which a token would be generated and stored as 'token.pickle' to avoid multiple authentications.

All the tasks would be completed automatically as per rules set.

# Database Integration
sqlite3 is used to store the filtered mails. 
'mails.db' is the source of the relational database. Table 'mails' is created and the filtered mails are stored in a relational format.



## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sujith-perikila-074699151/)



