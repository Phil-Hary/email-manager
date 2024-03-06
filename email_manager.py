from utils import CLI
from gmail_client import GmailClient

class EmailManager:
    def __init__(self):
        self.__is_authorized = False

    def pre_authorization_command_executor(self, command):
        if command == "1":
            self.email_client = GmailClient()
            self.email_client.authorize()
            self.__is_authorized = True
    
    def post_authorization_command_executor(self, command):
        if command == "1":
            self.email_client.fetch_emails()
    
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
            self.display_main_menu()
            choice = input()

            if choice == "0":
                break
                
            self.execute_command(choice)


if __name__ == "__main__": 
    email_manager = EmailManager()
    email_manager.driver()