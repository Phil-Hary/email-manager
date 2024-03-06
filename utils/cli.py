class CLI:
    @staticmethod
    def display(content):
        print(content)
    
    @staticmethod
    def display_menu(menu_options):

        for idx, menu_option in enumerate(menu_options):
            CLI.display(f"{idx + 1}. {menu_option}")
        
        CLI.display("0. Exit")
