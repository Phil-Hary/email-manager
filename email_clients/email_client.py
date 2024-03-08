from abc import ABC, abstractmethod

class EmailClient(ABC):
    """
        This is the base abstract class for all the email clients. Any email client must
        inherit this and override the abstract methods
    """
    @abstractmethod
    def authorize(self):
        """
            Description: This method must be overridden and defined with the logic to authorize the user
        """
        pass

    @abstractmethod
    def fetch_emails(self):
        """
            Description: This method must be overridden and defined with the logic to fetch the user emails
        """
        pass

    @abstractmethod
    def mark_emails_as_read():
        """
            Description: This method must be overridden and defined with the logic to mark the email as read
        """
        pass
    
    @abstractmethod
    def mark_emails_as_unread():
        """
            Description: This method must be overridden and defined with the logic to mark the email as unread
        """
        pass
    
    @abstractmethod
    def move_emails():
        """
            Description: This method must be overridden and defined with the logic to move the emails
        """
        pass

    