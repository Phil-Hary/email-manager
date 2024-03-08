import os
import pickle
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from .email_client import EmailClient

from constants import GMAIL_ATTRIBUTES_MAPPING, GMAIL_EMAIL_MARK_AS_PAYLOAD
from exceptions import AppError

class GmailClient(EmailClient):
    def __init__(self):
        self.credentials = None
        self.email_address = None
        self.labels = []

    def authorize(self, email_manager):
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
                        'https://www.googleapis.com/auth/gmail.modify'
                    ])


                credentials = flow.run_local_server(port=0)
                self.credentials = credentials

        with open('token.pickle', 'wb') as token:
            pickle.dump(self.credentials, token)
        
        email_address = self.get_email_address()
        email_manager.set_email_address(email_address)

    
    def initialize_service(self):
        self.service = build('gmail', 'v1', credentials=self.credentials)
    
    def get_email_address(self):
        # self.initialize_service()
        # email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']

        email_address = "augustin9940648860@gmail.com"
        return email_address

    def fetch_email_details(self, email_address, message_id):
        response = requests.get(
        url=f"https://gmail.googleapis.com/gmail/v1/users/{email_address}/messages/{message_id}",
            params={
                "access_token": self.credentials.token
            },
            headers={
                "Accept": "application/json"
            }
        )

        response = response.json()
        message_headers = response.get("payload", {}).get("headers", [])

        email_details = {
            "message_id": message_id
        }

        for message_header in message_headers:
            if message_header.get("name") in GMAIL_ATTRIBUTES_MAPPING.keys():
                email_details[GMAIL_ATTRIBUTES_MAPPING[message_header.get("name")]] = message_header.get("value")

        return email_details


    def fetch_emails(self, email_address):
        request = Request()
        if self.credentials.refresh_token:
            self.credentials.refresh(request)

    
        response = requests.get(
            url=f"https://gmail.googleapis.com/gmail/v1/users/{email_address}/messages",
            params={
                "access_token": self.credentials.token,
                "maxResults": 10,
                "q": 'in:inbox'
            },
            headers={
                "Accept": "application/json"
            }
        )

        if not response.ok:
            raise AppError(f"Fetchin emails failed with code {response.status_code}")

        response = response.json()
        messages = response.get("messages", [])

        message_ids = [message.get("id") for message in messages]
        return message_ids
    
    def mark_email(self, email_address, message_ids, mode):
        payload = {
            "ids": message_ids,
            **GMAIL_EMAIL_MARK_AS_PAYLOAD.get(mode)
        }

        response = requests.post(
            url=f"https://www.googleapis.com/gmail/v1/users/{email_address}/messages/batchModify?access_token={self.credentials.token}",
            headers={
                "Accept": "application/json"
            },
            json=payload
        )

        if not response.ok:
            raise AppError(f"Marking email as read failed with code {response.status_code}")
    

    
    def mark_emails_as_read(self, email_address, message_ids):
        self.mark_email(email_address, message_ids, "READ")
    
    def mark_emails_as_unread(self, email_address, message_ids):
        self.mark_email(email_address, message_ids, "UNREAD")
    
    def get_location_label_id(self, email_address, location):
        self.labels = [{'id': 'Label_9127678679863354574', 'name': 'Secondary', 'type': 'user'}]

        if not len(self.labels):
            response = requests.get(
                url=f"https://www.googleapis.com/gmail/v1/users/{email_address}/labels",
                params={
                    "access_token": {self.credentials.token}
                },
                headers={
                    "Accept": "application/json"
                }
            )

            if not response.ok:
                raise AppError(f"An error occurred while fetching labels with code {response.status_code}")

            data = response.json()

            labels = data.get("labels", [])
            self.labels = labels

        for label in self.labels:
            if label["name"] == location:
                return label["id"]
    
    def move_emails(self, email_address, message_ids, location):
        label_id = self.get_location_label_id(email_address, location)

        if not label_id:
            raise AppError("The provided location is not found in your email account")

        response = requests.post(
            url=f"https://www.googleapis.com/gmail/v1/users/{email_address}/messages/batchModify?access_token={self.credentials.token}",
            headers={
                "Accept": "application/json"
            },
            json={
                "ids": message_ids,
                "addLabelIds": [label_id],
                "removeLabelIds": ["INBOX"]
            }
        )

        if not response.ok:
            raise AppError(f"An error occurred while moving the emails with code {response.status_code}")

