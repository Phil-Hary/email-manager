from abc import ABC, abstractmethod

class BaseInterface(ABC):
    """
        This is the base abstract class for all the interfaces. Any user interface must
        inherit this and override the abstract methods
    """
    @abstractmethod
    def display_menu():
        """
            Description: This method must be overridden and defined with the logic to display the menu for a particular screen
        """
        pass

    @abstractmethod
    def command_handler():
        """
            Description: This method must be overridden and defined with the logic to handle the menu options
        """
        pass