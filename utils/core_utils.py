from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import Session

from models import Account, Email

from .cli import CLI
from .common_utils import CommonUtils
from .db_utils import DBUtils


class CoreUtils:
    """
        This class holds the core util methods which are used to perform core app operations
    """
    @staticmethod
    def get_new_email_ids(email_ids):
        """
            Description: This method returns back the email_ids which is not in the db
        """
        new_email_ids = []
        engine = DBUtils.get_engine()

        
        with Session(engine) as session:
            for email_id in email_ids:
                email = session.query(Email).filter_by(message_id=email_id).first()
                
                if not email:
                    new_email_ids.append(email_id)
                    
        return new_email_ids

    @staticmethod
    def save_email_details(email_address, email_details):
        """
            Description: This method saves the email detais to the database
        """
        engine = DBUtils.get_engine()

        with Session(engine) as session:
            account = session.query(Account).filter_by(email_id=email_address).first()
            
            if not account:
                account = Account(email_id=email_address)
                session.add(account)
                session.commit()
            
            email_details["account_id"] = account.id
            email_details["date"] = CommonUtils.convert_date_string_to_object(email_details["date"])
            
            email = Email(**email_details)
            session.add(email)
            session.commit()
        
    @staticmethod
    def fetch_and_save_emails(email_manager):
        """
            Description: This is the driver method which fetches and saves the emails to DB.
            
            Flow:
                - First fetches the email ids from the email client
                - Then identifies the email ids which is not already saved to 
                  the DB to prevent redundant email detail calls
                - For the new email id parallel fetches the email details
                - Finally saves the new email details to the DB
        """
        email_address = email_manager.get_email_address()
        email_client = email_manager.get_email_client()
        
        email_ids = email_client.fetch_emails(email_address)
        new_email_ids = CoreUtils.get_new_email_ids(email_ids)

        CLI.display(f"Fetched {len(new_email_ids)} new emails")

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    email_client.fetch_email_details, email_address, email_id
                ) for email_id in new_email_ids
            ]

            for future in as_completed(futures):
                email_details = future.result()
                CoreUtils.save_email_details(email_address, email_details)
