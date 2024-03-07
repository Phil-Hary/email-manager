from datetime import datetime

class CommonUtils:

    @staticmethod
    def convert_date_string_to_object(date_string, date_format="%a, %d %b %Y %H:%M:%S %z"):
        date_time_obj = datetime.strptime(date_string, date_format)
        return date_time_obj