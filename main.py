from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_940888710000-4gpuej2kf44nvh7ndou5q98vor41ipql.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

message = MIMEMultipart()
message['to'] = 'recipient@example.com'
message['subject'] = 'Draft Email Test1'
message.attach(MIMEText('This is the body of the draft email'))

# convert the message to bytes
your_draft_email_bytes = message.as_bytes()


try:
    service = build('gmail', 'v1', credentials=creds)

    message = {
        'message': {
            'raw': base64.urlsafe_b64encode(your_draft_email_bytes).decode()
        }
    }

    draft = service.users().drafts().create(userId='me', body=message).execute()
    print(F'Draft created with Id: {draft["id"]}')
    draft_url = f"https://mail.google.com/mail/u/0/#drafts?compose={draft['message']['id']}"
    print(F'Draft URL: {draft_url}')
    # print(draft)
    # print(dir(draft))

except HttpError as error:
    print(F'An error occurred: {error}')
    draft = None
