from colorama import Fore, Style

from enums import DisplayModeEnum

class CLI:
    @staticmethod
    def display(content, mode=DisplayModeEnum.DEFAULT):
        color = getattr(Fore, mode.value)
        print(color + content)
        print(Style.RESET_ALL, end="")
    
    @staticmethod
    def display_menu(menu_options):

        for idx, menu_option in enumerate(menu_options):
            CLI.display(f"{idx + 1}. {menu_option}", DisplayModeEnum.MENU)
        
        CLI.display("0. Exit", DisplayModeEnum.MENU)
        print(Style.RESET_ALL, end="")

