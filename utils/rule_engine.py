from datetime import datetime, timedelta

from constants import GMAIL_ATTRIBUTES_MAPPING, STRING_PREDICATE_MAPPING, DATE_PREDICATE_MAPPING
from models import Email, Account
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from exceptions import AppError

from .cli import CLI
from .db_utils import DBUtils

class RuleEngine:
    """
        This class holds the util methods to execute the rules
    """
    @staticmethod
    def get_overall_predicate_operator(predicate):
        """
            Description: This method returns the equivalent operator for the overall predicate
        """
        predicate = predicate.lower()
        if predicate == "all":
            return "AND"
        elif predicate == "any":
            return "OR"
        else:
            raise AppError("Rules collection predicate can be either All or Any")

    @staticmethod
    def get_condition_from_rule(rule, idx, parameters):
        """
            Description: This method converts a json rule from the rule.json to equivalent sql condition
        """
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
        """
            Description: This method iteratively coverts the rules into the appropriate sql condition
        """
        conditions = []
        
        for idx, rule in enumerate(rules):
            condition = RuleEngine.get_condition_from_rule(rule, idx, parameters)
            conditions.append(condition)
        
        overall_predicate_operator = RuleEngine.get_overall_predicate_operator(overall_predicate)
        where_clause = f" {overall_predicate_operator} ".join(conditions)

        return where_clause

    @staticmethod
    def run_query(email_address, where_clause, parameters):
        """
            Description: This method runs the constructed query in the database and returns the result
        """
        engine = DBUtils.get_engine()
        data = None

        with Session(engine) as session:
            data = (
                session.query(Email)
                .join(Account, Email.account_id == Account.id)
                .filter(Account.email_id == email_address)
                .filter(text(where_clause))
                .params(**parameters)
                .all()
            )

        return data

    @staticmethod
    def execute_rules(rules, email_address):
        """
            Description: This method executes a rule by first converting all the rules to where clause and then
            runs the query in the DB
        """
        predicate = rules.get("predicate", None)
        rules = rules.get("rules", None)
        parameters = {}

        if not predicate:
            raise AppError("Encountered an invalid rule predicate")
        
        try:
            where_clause = RuleEngine.rules_to_where_clause_converter(rules, predicate, parameters)
            query_data = RuleEngine.run_query(email_address, where_clause, parameters)
        except AppError as e:
            raise e
        except Exception as e:
            raise AppError(f"An error occurred during rule execution - {str(e)}")

        return query_data


    @staticmethod
    def implement_action(email_manager, message_ids, actions):
        """
            Description: This method executes the action on the emails selected by the rules
        """
        email_client = email_manager.get_email_client()
        email_address = email_manager.get_email_address()

        for action_meta in actions:
            action = action_meta.get("action")

            if action == "Mark as read":
                email_client.mark_emails_as_read(email_address, message_ids)
                CLI.display("Emails marked as read")
            elif action == "Mark as unread":
                email_client.mark_emails_as_unread(email_address, message_ids)
                CLI.display("Emails marked as unread")
            elif action == "Move":
                location = action_meta.get("location")

                if not location:
                    raise AppError("Location to be moved must be valid")
                
                email_client.move_emails(email_address, message_ids, location)
                CLI.display(f"Emails moved to {location}")
            
    @staticmethod
    def execute(rule, email_manager):
        """
            Description: This the driver method which get the rule selected by the user and processes it
            Flow:
                - Extracts the rule and the action from the rule definition
                - Converts the rules into a where clause and constructs the query
                - Executes the query on the DB
                - If the query return any emails, implements the actions on them

        """
        rules = rule.get("rule", {})
        actions = rule.get("actions", [])
        email_address = email_manager.get_email_address()

        emails = RuleEngine.execute_rules(rules, email_address)
        
        if not len(emails):
            raise AppError("Cannot find any emails satifisying the selected rule")

        message_ids = [] 

        for email in emails:
            message_ids.append(str(email.message_id))
        
        RuleEngine.implement_action(email_manager, message_ids, actions)
        CLI.display("Rule execution completed")

