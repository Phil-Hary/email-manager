import json

from enums import DisplayModeEnum
from exceptions import AppError
from utils import CLI, RuleEngine

from .base_interface import BaseInterface

class ActionsInterface(BaseInterface):
    """
        This class handles the actions interface
    """
    def fetch_rules_from_file(self):
        """
            Description: This method fetches the rules from rules.json file
        """
        try:
            with open("rules.json", 'r') as file:
                self.rules = json.load(file)
        except Exception as e:
            raise AppError(f"An error occurred while reading rules.json - {str(e)}", hard_error=True)
    
    def get_rule_names(self):
        """
            Description: This method fetches the rules names to be displayed in the menu
        """
        rule_names = []

        self.fetch_rules_from_file()
        rules = self.rules.get("rules", [])

        for rule in rules:
            rule_names.append(rule.get("name"))
        
        return rule_names

    def display_menu(self):
        """
            Description: This method displays the actions menu
        """
        CLI.display("Choose a rule to proceed")
        rule_names = self.get_rule_names()
        CLI.display_menu(rule_names)

    def command_handler(self, email_manager, command):
        """
            Description: This method handles the command provided by the user
        """
        CLI.display(f"Executing rule {command}", DisplayModeEnum.ADMIN)
        rules = self.rules.get("rules", [])
        if not len(rules):
            raise AppError("Encoutered invalid rules")
        
        rule = rules[int(command) - 1]

        RuleEngine.execute(rule, email_manager)
            