import pytest

from datetime import datetime

from exceptions import AppError
from utils import CommonUtils

class TestCommonUtils:
    @pytest.fixture
    def common_utils_instance(self):
        return CommonUtils()

    def test_convert_datestring_to_object(self, common_utils_instance):
        date_string = "Thu, 07 Mar 2024 20:00:00 +0000"
        expected_date = datetime(2024, 3, 7, 20, 0, 0)

        assert common_utils_instance.convert_date_string_to_object(date_string).replace(tzinfo=None) == expected_date.replace(tzinfo=None)
    
    def test_convert_datestring_to_object_with_valid_format(self, common_utils_instance):
        date_string = "Thu, 07 Mar 2024"
        expected_date = datetime(2024, 3, 7)
        date_string_format = "%a, %d %b %Y"

        assert common_utils_instance.convert_date_string_to_object(date_string, date_string_format).replace(tzinfo=None) == expected_date.replace(tzinfo=None)
    
    def test_convert_datestring_to_object_with_invalid_format(self, common_utils_instance):
        date_string = "Thu, 07 Mar 2024"
        date_string_format = "%a, %d %b"

        with pytest.raises(AppError):
            common_utils_instance.convert_date_string_to_object(date_string, date_string_format)
    
    def test_convert_datestring_to_object_with_invalid_date(self, common_utils_instance):
        date_string = "Thu, 07 Mar"
        date_string_format = "%a, %d %b %Y"

        with pytest.raises(AppError):
            common_utils_instance.convert_date_string_to_object(date_string, date_string_format)
            
            