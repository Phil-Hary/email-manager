from constants import GMAIL_ATTRIBUTES_MAPPING, STRING_PREDICATE_MAPPING
from models import Email
from sqlalchemy.orm import Session
from .db_utils import DBUtils
from sqlalchemy.sql import text

from exceptions import AppError

class RuleEngine:
    @staticmethod
    def get_overall_predicate_operator( predicate):
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

        PREDICATE_MAPPING = STRING_PREDICATE_MAPPING if field_type == "string" else STRING_PREDICATE_MAPPING

        if "contain" in predicate:
            parameters[placeholder] = f"%{value}%"
            value = f":{placeholder}"
            

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

        email_address = "harrisonharry01@gmail.com"
        data = None

        with Session(engine) as session:
            data = session.query(Email).filter(text(where_clause)).params(**parameters).all()
        
        print(data)
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
        for action_meta in actions:
            action = action_meta.get("action")

            if action == "Mark as read":
                print("Executing")
                email_manager.email_client.mark_emails_as_read((message_ids))
            
        

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
        
        print(message_ids)
        
        RuleEngine.implement_action(email_manager, message_ids, actions)

