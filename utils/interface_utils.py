from enums import InterfaceEnum

from interfaces import ActionsInterface, PreAuthInterface, PostAuthInterface

class InterfaceUtils:
    @staticmethod
    def get_interface(current_interface):
        if current_interface == InterfaceEnum.PRE_AUTH:
            return PreAuthInterface()
        elif current_interface == InterfaceEnum.POST_AUTH:
            return PostAuthInterface()
        elif current_interface == InterfaceEnum.ACTIONS:
            return ActionsInterface()