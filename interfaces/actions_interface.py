import json

from utils import CLI, RuleEngine
from enums import InterfaceEnum

from gmail_client import GmailClient

from .base_interface import BaseInterface

class ActionsInterface(BaseInterface):
    def fetch_rules_from_file(self):
        with open("rules.json", 'r') as file:
            self.rules = json.load(file)
    
    def get_rule_names(self):
        rule_names = []

        self.fetch_rules_from_file()
        rules = self.rules.get("rules", [])

        for rule in rules:
            rule_names.append(rule.get("name"))
        
        return rule_names

    def display_menu(self):
        CLI.display("Choose a rule to proceed")
        rule_names = self.get_rule_names()
        CLI.display_menu(rule_names)

    def command_handler(self, email_manager, command):
        rules = self.rules.get("rules", [])
        if not len(rules):
            print("Error")
        
        rule = rules[int(command) - 1]

        RuleEngine.execute(rule, email_manager)
            