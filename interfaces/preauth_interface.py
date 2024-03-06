from utils import CLI
from enums import InterfaceEnum

from gmail_client import GmailClient

from .base_interface import BaseInterface

class PreAuthInterface(BaseInterface):
    def display_menu(self):
        CLI.display("Choose an email service provider to continue")
        CLI.display_menu(["Gmail"])

    def command_handler(self, email_manager, command):
        if command == "1":
            email_manager.email_client = GmailClient()
            email_manager.email_client.authorize()
            email_manager.set_is_authorized(True)
            email_manager.set_current_interface(InterfaceEnum.POST_AUTH)

            