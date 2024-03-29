GMAIL_ATTRIBUTES_MAPPING = {
    "From": "from_email_id",
    "Delivered-To": "to_email_id",
    "Subject": "subject",
    "Date": "date"
}

GMAIL_EMAIL_MARK_AS_PAYLOAD = {
    "READ": {
        "addLabelIds": [],
        "removeLabelIds": ["UNREAD"]
    },
    "UNREAD": {
        "addLabelIds": ["UNREAD"],
        "removeLabelIds": []
    }
}

GMAIL_SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.modify'
]

GMAIL_SCERET_FILE_NAME = "client_secrets.json"
GMAIL_NUMBER_OF_EMAILS = 30

INTERFACES = {
    "PRE_AUTH": "PRE_AUTH",
    "POST_AUTH": "POST_AUTH",
    "ACTIONS": "ACTIONS"
}

STRING_PREDICATE_MAPPING = {
    "contains": "LIKE",
    "does not contain": "NOT LIKE",
    "equals": "=",
    "not equals": "!="
}

DATE_PREDICATE_MAPPING = {
    "greater than": "BETWEEN",
    "lesser than": "BETWEEN"
}

SUPPORTED_EMAIL_PROVIDERS = ["Gmail"]

