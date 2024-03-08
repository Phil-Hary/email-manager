from enums import InterfaceEnum
from utils import CLI

from .base_interface import BaseInterface

class PostAuthInterface(BaseInterface):
    """
        This class handles the post auth interface
    """
    def display_menu(self):
        """
            Description: This method displays the post auth menu
        """
        CLI.display("Choose an operation to continue")
        CLI.display_menu(["Fetch emails", "Actions"])

    def command_handler(self, email_manager, command):
        """
            Description: This method handles the command provided by the user
        """
        if command == "1":
            email_manager.fetch_emails()
        elif command == "2":
            #changing the interface actions interface
            email_manager.set_current_interface(InterfaceEnum.ACTIONS)
            