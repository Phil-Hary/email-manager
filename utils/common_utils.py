from datetime import datetime

from exceptions import AppError

class CommonUtils:

    @staticmethod
    def convert_date_string_to_object(date_string, date_format="%a, %d %b %Y %H:%M:%S %z"):
        try:
            date_time_obj = datetime.strptime(date_string, date_format)
        except Exception:
            raise AppError("An error occurred during date conversion")
        
        return date_time_obj