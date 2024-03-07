import pytest
import requests_mock

from unittest.mock import MagicMock

from email_clients import GmailClient
from utils import CommonUtils

class TestGmailClient:
    @pytest.fixture
    def gmail_client_instance(self):
        return GmailClient()
    
    def test_fetch_email_details(self, gmail_client_instance):
        with requests_mock.Mocker() as mocker:

            email_address = "receiver@gmail.com"
            message_id = "em_mail_001"

            mock_response = {
                "payload": {
                    "headers": [
                        {
                            "name": "From",
                            "value": "sender@gmail.com"
                        },
                        {
                            "name": "Delivered-To",
                            "value": "receiver@gmail.com"
                        },
                        {
                            "name": "Subject",
                            "value": "Test email"
                        },
                        {
                            "name": "Date",
                            "value": "Thu, 07 Mar 2024 20:00:00 +0000"
                        }
                    ]
                }
            }

            mocker.get(
                f"https://gmail.googleapis.com/gmail/v1/users/{email_address}/messages/{message_id}",
                json=mock_response
            )

            gmail_client_instance.credentials = MagicMock()
            gmail_client_instance.credentials.token = "mock_token"

            email_details = gmail_client_instance.fetch_email_details(email_address, message_id)

            expected_response = {
                "message_id": message_id,
                "from_email_id": "sender@gmail.com",
                "to_email_id": "receiver@gmail.com",
                "subject": "Test email",
                "date": CommonUtils.convert_date_string_to_object("Thu, 07 Mar 2024 20:00:00 +0000")
            }

            assert sorted(email_details) == sorted(expected_response)

    def test_fetch_emails(self, gmail_client_instance):
        with requests_mock.Mocker() as mocker:

            email_address = "receiver@gmail.com"
            message_id = "em_mail_001"

            mock_response = {
                "messages": [
                    {
                        "id": "message_1",
                    },
                    {
                        "id": "message_2",
                    },
                    {
                        "id": "message_3",
                    },
                    {
                        "id": "message_4",
                    }
                ]
                
            }

            mocker.get(
                f"https://gmail.googleapis.com/gmail/v1/users/{email_address}/messages",
                json=mock_response
            )

            gmail_client_instance.credentials = MagicMock()
            gmail_client_instance.credentials.token = "mock_token"

            email_ids = gmail_client_instance.fetch_emails(email_address)

            expected_response = ["message_1", "message_2", "message_3", "message_4"]

            assert email_ids == expected_response
    
    def test_get_location_label_id(self, gmail_client_instance):
        mock_label_id = 'Label_9127678679863354574'
        gmail_client_instance.labels = MagicMock()
        gmail_client_instance.labels = [{'id': mock_label_id, 'name': 'Secondary', 'type': 'user'}]
        email_address = "receiver@gmail.com"
        location = "Secondary"

        label_id = gmail_client_instance.get_location_label_id(email_address, location)

        assert mock_label_id == label_id