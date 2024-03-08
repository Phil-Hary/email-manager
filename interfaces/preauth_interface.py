from constants import SUPPORTED_EMAIL_PROVIDERS
from email_clients import GmailClient
from enums import InterfaceEnum
from utils import CLI

from .base_interface import BaseInterface

class PreAuthInterface(BaseInterface):
    """
        This class handles the pre auth interface
    """
    def display_menu(self):
        """
            Description: This method displays the pre auth menu
        """
        CLI.display("Choose an email service provider to continue")
        CLI.display_menu(SUPPORTED_EMAIL_PROVIDERS)

    def command_handler(self, email_manager, command):
        """
            Description: This method handles the command provided by the user
        """
        if command == "1":
            #intialising the email client
            email_client = GmailClient()
            email_manager.set_email_client(email_client)

            #authorizing the user
            email_client.authorize(email_manager)
            email_manager.set_is_authorized(True)

            #changing the interface to post auth interface
            email_manager.set_current_interface(InterfaceEnum.POST_AUTH)

            