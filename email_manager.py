from enums import InterfaceEnum, DisplayModeEnum
from exceptions import AppError
from utils import CLI, InterfaceUtils, CoreUtils

class EmailManager:
    """
        This is the entrypoint to the application, and drives the whole flow
    """
    def __init__(self):
        self._is_authorized = False
        self._current_interface = InterfaceEnum.PRE_AUTH
        
        self._email_client = None
        self._email_address = None
    
    def set_current_interface(self, current_interface):
        self._current_interface = current_interface
    
    def set_is_authorized(self, is_authorised):
        self._is_authorized = is_authorised
    
    def set_email_address(self, email_address):
        self._email_address = email_address
    
    def get_email_address(self):
        if not self._email_address:
            self._email_address = self._email_client.get_email_address()
        return self._email_address

    def get_email_client(self):
        if not self._email_client:
            raise AppError("Email client is not yet initialized")
        
        return self._email_client

    def set_email_client(self, email_client):
        self._email_client = email_client
    
    def fetch_emails(self):
        CoreUtils.fetch_and_save_emails(self)
    
    def driver(self):
        """
            Description: This is the driver method which diplays the different menus and capture user choices
        """
        while True:
            try:
                interface = InterfaceUtils.get_interface(self._current_interface)
                interface.display_menu()

                choice = input()

                if choice == "0":
                    break
                    
                interface.command_handler(self, choice)
            except AppError as e:
                CLI.display(e.message, DisplayModeEnum.ERROR)

                #stops the execution in case of hard error
                if e.hard_error:
                    break


if __name__ == "__main__": 
    email_manager = EmailManager()
    email_manager.driver()