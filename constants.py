GMAIL_ATTRIBUTES_MAPPING = {
    "From": "from_email_id",
    "Delivered-To": "to_email_id",
    "Subject": "subject",
    "Date": "date"
}

INTERFACES = {
    "PRE_AUTH": "PRE_AUTH",
    "POST_AUTH": "POST_AUTH",
    "ACTIONS": "ACTIONS"
}

STRING_PREDICATE_MAPPING = {
    "contains": "LIKE",
    "does not contain": "NOT LIKE",
    "equals": "==",
    "not equals": "!="
}

DATE_PREDICATE_MAPPING = {
    "greater than": "BETWEEN",
    "lesser than": "BETWEEN"
}
