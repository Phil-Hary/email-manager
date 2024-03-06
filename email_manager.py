from utils import CLI, InterfaceUtils
from gmail_client import GmailClient

from enums import InterfaceEnum


class EmailManager:
    def __init__(self):
        self.__is_authorized = False
        self._is_authorized = False
        self._current_interface = InterfaceEnum.PRE_AUTH
        
        self.email_client = None
    
    def set_current_interface(self, current_interface):
        self._current_interface = current_interface
    
    def set_is_authorized(self, is_authorised):
        self._is_authorized = is_authorised

    def pre_authorization_command_executor(self, command):
        if command == "1":
            self.email_client = GmailClient()
            self.email_client.authorize()
            self.__is_authorized = True
    
    def post_authorization_command_executor(self, command):
        if command == "1":
            self.email_client.fetch_emails()
        elif command == "2":
            self.__actions_activated = True 
            CLI.display("Choose an action to proceed")
            CLI.display_menu(["Mark as read", "Move"])

    def execute_command(self, command):
        if not self.__is_authorized:
            self.pre_authorization_command_executor(command)
        else:
            self.post_authorization_command_executor(command)
    
    def display_pre_authorization_menu(self):
        CLI.display("Choose an email service provider to continue")
        CLI.display_menu(["Gmail"])
    
    def display_post_authorization_menu(self):
        CLI.display("Choose an operation to continue")
        CLI.display_menu(["Fetch emails", "Actions"])

    def display_main_menu(self):
        if not self.__is_authorized:
            self.display_pre_authorization_menu()
        else:
            self.display_post_authorization_menu()

    def driver(self):
        while True:
            interface = InterfaceUtils.get_interface(self._current_interface)
            interface.display_menu()

            choice = input()

            if choice == "0":
                break
                
            interface.command_handler(self, choice)


if __name__ == "__main__": 
    email_manager = EmailManager()
    email_manager.driver()