import os
import pickle
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from email_client import EmailClient

from constants import MESSAGE_DATA, GMAIL_ATTRIBUTES_MAPPING

class GmailClient(EmailClient):
    def __init__(self):
        self.credentials = None
        self.email_address = None

    def authorize(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=[
                        'openid',
                        'https://www.googleapis.com/auth/userinfo.email',
                        'https://www.googleapis.com/auth/gmail.readonly'
                    ])


                credentials = flow.run_local_server(port=0)
                self.credentials = credentials

        with open('token.pickle', 'wb') as token:
            pickle.dump(self.credentials, token)
    
    def initialize_service(self):
        self.service = build('gmail', 'v1', credentials=self.credentials)
    
    def get_email_address(self):
        if not self.email_address:
            self.initialize_service()
            self.email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']

        return self.email_address

    def fetch_emails(self):
        self.get_email_address()
        print(self.credentials.__dict__)
        print(self.email_address)
        
        request = Request()
        if self.credentials.refresh_token:
            self.credentials.refresh(request)

    
        # response = requests.get(
        #     url=f"https://gmail.googleapis.com/gmail/v1/users/{self.email_address}/messages?access_token={self.credentials.token}",
        #     headers={
        #         "Accept": "application/json"
        #     }
        # )

        # response = response.json()
        # messages = response.get("messages", [])

        # {'id': '18e11866023b6af8', 'threadId': '18e11866023b6af8'}

        # message_id = "18e11866023b6af8"

        # response = requests.get(
        # url=f"https://gmail.googleapis.com/gmail/v1/users/{self.email_address}/messages/{message_id}?access_token={self.credentials.token}",
        #     headers={
        #         "Accept": "application/json"
        #     }
        # )


        message_headers = MESSAGE_DATA.get("payload", {}).get("headers", [])

        extracted_data = {
            "message_id": "18e11866023b6af8"
        }

        for message_header in message_headers:
            if message_header.get("name") in GMAIL_ATTRIBUTES_MAPPING.keys():
                extracted_data[GMAIL_ATTRIBUTES_MAPPING[message_header.get("name")]] = message_header.get("value")


        print(extracted_data)
        
