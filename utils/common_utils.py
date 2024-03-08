from datetime import datetime

from exceptions import AppError

class CommonUtils:
    """
        This class holds the common util methods
    """
    @staticmethod
    def convert_date_string_to_object(date_string, date_format="%a, %d %b %Y %H:%M:%S %z"):
        """
            Description: This method converts the date string to a datetime object
        """
        try:
            date_time_obj = datetime.strptime(date_string, date_format)
        except Exception:
            raise AppError("An error occurred during date conversion")
        
        return date_time_obj