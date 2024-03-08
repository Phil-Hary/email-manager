from colorama import Fore, Style

from enums import DisplayModeEnum

class CLI:
    """
        This is class holds the static methods to interact with the CLI
    """
    @staticmethod
    def display(content, mode=DisplayModeEnum.DEFAULT):
        """
            Description: This method prints content on the CMD based on the provided mode
        """
        color = getattr(Fore, mode.value)
        print(color + content)
        print(Style.RESET_ALL, end="")
    
    @staticmethod
    def display_menu(menu_options):
        """
            Description: This method displays the provided menu on the CMD
        """
        for idx, menu_option in enumerate(menu_options):
            CLI.display(f"{idx + 1}. {menu_option}", DisplayModeEnum.MENU)
        
        CLI.display("0. Exit", DisplayModeEnum.MENU)
        print(Style.RESET_ALL, end="")

