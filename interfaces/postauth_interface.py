from utils import CLI
from enums import InterfaceEnum

from gmail_client import GmailClient

from .base_interface import BaseInterface

class PostAuthInterface(BaseInterface):
    def display_menu(self):
        CLI.display("Choose an operation to continue")
        CLI.display_menu(["Fetch emails", "Actions"])

    def command_handler(self, email_manager, command):
        if command == "1":
            email_manager.email_client.fetch_emails()
        elif command == "2":
            email_manager.set_current_interface(InterfaceEnum.ACTIONS)
            