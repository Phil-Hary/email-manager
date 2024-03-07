from abc import ABC, abstractmethod

class EmailClient(ABC):
    @abstractmethod
    def authorize(self):
        pass

    @abstractmethod
    def fetch_emails(self):
        pass