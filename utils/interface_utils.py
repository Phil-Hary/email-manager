from enums import InterfaceEnum

from interfaces import ActionsInterface, PreAuthInterface, PostAuthInterface

class InterfaceUtils:
    """
        This class holds the util methods to power the interface
    """
    @staticmethod
    def get_interface(current_interface):
        """
            Description: This is a factory method, which creates and returns the interface object
            based on the provided current interface
        """
        if current_interface == InterfaceEnum.PRE_AUTH:
            return PreAuthInterface()
        elif current_interface == InterfaceEnum.POST_AUTH:
            return PostAuthInterface()
        elif current_interface == InterfaceEnum.ACTIONS:
            return ActionsInterface()