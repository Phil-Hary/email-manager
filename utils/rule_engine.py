from datetime import datetime, timedelta

from constants import GMAIL_ATTRIBUTES_MAPPING, STRING_PREDICATE_MAPPING, DATE_PREDICATE_MAPPING
from models import Email, Account
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from exceptions import AppError

from .cli import CLI
from .db_utils import DBUtils

class RuleEngine:
    @staticmethod
    def get_overall_predicate_operator(predicate):
        predicate = predicate.lower()
        if predicate == "all":
            return "AND"
        elif predicate == "any":
            return "OR"
        else:
            raise AppError("Rules collection predicate can be either All or Any")

    @staticmethod
    def get_condition_from_rule(rule, idx, parameters):
        field_name = rule["field_name"]
        predicate = rule["predicate"]
        value = rule["value"]
        field_type = rule["field_type"]

        placeholder = f"value_{idx + 1}"
        parameters[placeholder] = value
        PREDICATE_MAPPING = {}


        if field_type == "string":
            PREDICATE_MAPPING = STRING_PREDICATE_MAPPING
            if "contain" in predicate:
                parameters[placeholder] = f"%{value}%"
                value = f":{placeholder}"
            else:
                parameters[placeholder] = f"{value}"
                value = f":{placeholder}"

        elif field_type == "date":
            PREDICATE_MAPPING = DATE_PREDICATE_MAPPING
            unit = rule["unit"]
            unit = unit.lower()
            delta = timedelta(days=1)
            value = int(value)

            if unit == "days":
                delta = timedelta(days=value)
            elif unit == "months":
                delta = timedelta(days=value * 30)

            end_date = datetime.now()
            start_date = end_date - delta

            placeholder = f":start_date AND :end_date"
            parameters["start_date"] = start_date.strftime('%Y-%m-%d')
            parameters["end_date"] = end_date.strftime('%Y-%m-%d')
            value = placeholder

        return f"{GMAIL_ATTRIBUTES_MAPPING[field_name]} {PREDICATE_MAPPING[predicate.lower()]} {value}"

    @staticmethod
    def rules_to_where_clause_converter(rules, overall_predicate, parameters):
        conditions = []
        
        for idx, rule in enumerate(rules):
            condition = RuleEngine.get_condition_from_rule(rule, idx, parameters)
            conditions.append(condition)
        
        overall_predicate_operator = RuleEngine.get_overall_predicate_operator(overall_predicate)

        where_clause = f" {overall_predicate_operator} ".join(conditions)

        return where_clause

    @staticmethod
    def run_query( where_clause, parameters):
        engine = DBUtils.get_engine()
        data = None

        with Session(engine) as session:
            data = (
                session.query(Email)
                .join(Account, Email.account_id == Account.id)
                .filter(Account.email_id == "augustin9940648860@gmail.com")
                .filter(text(where_clause))
                .params(**parameters)
                .all()
            )

        for d in data:
            print(d.message_id)

        return data

    @staticmethod
    def execute_rules(rules):
        predicate = rules.get("predicate", None)
        rules = rules.get("rules", None)
        parameters = {}

        if not predicate:
            raise AppError("Encountered an invalid rule predicate")
        
        where_clause = RuleEngine.rules_to_where_clause_converter(rules, predicate, parameters)
        query_data = RuleEngine.run_query(where_clause, parameters)

        return query_data


    @staticmethod
    def implement_action(email_manager, message_ids, actions):
        email_client = email_manager.get_email_client()
        email_address = email_manager.get_email_address()

        for action_meta in actions:
            action = action_meta.get("action")

            if action == "Mark as read":
                email_client.mark_emails_as_read(email_address, message_ids)
                CLI.display("Emails marked as read")
            elif action == "Move":
                location = action_meta.get("location")

                if not location:
                    raise AppError("Location to be moved must be a valid")
                
                email_client.move_emails(email_address, message_ids, location)
                CLI.display(f"Emails moved to {location}")
            
        

    @staticmethod
    def execute(rule, email_manager):
        rules = rule.get("rule", {})
        actions = rule.get("actions", [])

        emails = RuleEngine.execute_rules(rules)
        
        if not len(emails):
            raise AppError("Cannot find any emails satifisying the selected rule")

        message_ids = [] 

        for email in emails:
            message_ids.append(str(email.message_id))
        
        RuleEngine.implement_action(email_manager, message_ids, actions)
        CLI.display("Rule execution completed")

