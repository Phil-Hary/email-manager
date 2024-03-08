import os
import pickle
import requests

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from constants import (
    GMAIL_ATTRIBUTES_MAPPING,
    GMAIL_EMAIL_MARK_AS_PAYLOAD,
    GMAIL_NUMBER_OF_EMAILS,
    GMAIL_SCERET_FILE_NAME,
    GMAIL_SCOPES
)
    
from exceptions import AppError

from .email_client import EmailClient

class GmailClient(EmailClient):
    """
        This is the EmailClient implemetation for Gmail
    """
    def __init__(self):
        self.credentials = None
        self.email_address = None
        self.labels = []

    def authorize(self, email_manager):
        """
            Description: This method authorises the user using google oauth'
        """
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GMAIL_SCERET_FILE_NAME,
                    scopes=GMAIL_SCOPES)


                credentials = flow.run_local_server(port=0)
                self.credentials = credentials

        with open('token.pickle', 'wb') as token:
            pickle.dump(self.credentials, token)
        
        email_address = self.get_email_address()
        email_manager.set_email_address(email_address)

    
    def initialize_service(self):
        """
            Description: This method intializes the service
        """
        self.service = build('gmail', 'v1', credentials=self.credentials)
    
    def get_email_address(self):
        """
            Description: This method fetches the user's email address
        """
        # self.initialize_service()
        # email_address = self.service.users().getProfile(userId='me').execute()['emailAddress']

        email_address = "augustin9940648860@gmail.com"
        return email_address

    def fetch_email_details(self, email_address, message_id):
        """
            Description: This method fetches an email's details
        """
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

        #extracting email details from the email to be persisted in the db
        message_headers = response.get("payload", {}).get("headers", [])

        email_details = {
            "message_id": message_id
        }

        for message_header in message_headers:
            if message_header.get("name") in GMAIL_ATTRIBUTES_MAPPING.keys():
                email_details[GMAIL_ATTRIBUTES_MAPPING[message_header.get("name")]] = message_header.get("value")

        return email_details

    def fetch_emails(self, email_address):
        """
            Description: This method fetches the user emails user gmail apis and retruns back the email ids
        """
        request = Request()
        if self.credentials.refresh_token:
            self.credentials.refresh(request)

    
        response = requests.get(
            url=f"https://gmail.googleapis.com/gmail/v1/users/{email_address}/messages",
            params={
                "access_token": self.credentials.token,
                "maxResults": GMAIL_NUMBER_OF_EMAILS,
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
        """
            Description: This method marks the email as read or unread based on the mode passed using gmail api
        """
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
        """
            Description: This method marks the email as read
        """
        self.mark_email(email_address, message_ids, "READ")
    
    def mark_emails_as_unread(self, email_address, message_ids):
        """
            Description: This method marks the email as unread
        """
        self.mark_email(email_address, message_ids, "UNREAD")
    
    def get_location_label_id(self, email_address, location):
        """
            Description: This method fetches the location label id, for the emails to moved to the apporpriate location.
            In a run, it caches the labels inorder to prevent redundant calls
        """
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
        """
            Description: This method moves the emails to the provided location
        """
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

