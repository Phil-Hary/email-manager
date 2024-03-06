from abc import ABC, abstractmethod

class BaseInterface(ABC):
    @abstractmethod
    def display_menu():
        pass

    @abstractmethod
    def command_handler():
        pass