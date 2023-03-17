from .test_helper_base import HelperTestCase
from financial_companion.helpers import convert_list_to_string


class ConvertListToStringHelperFunctionTestCase(HelperTestCase):
    """Test file for the convert_list_to_string helpers function"""

    def test_convert_valid_list_to_string(self):
        result: str = convert_list_to_string([1, 2, 3, 4, 5, 6])
        self.assertEqual("1, 2, 3, 4, 5, and 6", result)

    def test_convert_valid_list_with_length_1_to_string(self):
        result: str = convert_list_to_string([1])
        self.assertEqual("1", result)

    def test_convert_valid_list_with_length_2_to_string(self):
        result: str = convert_list_to_string([1, 2])
        self.assertEqual("1 and 2", result)

    def test_convert_valid_list_with_length_3_to_string(self):
        result: str = convert_list_to_string([1, 2, 3])
        self.assertEqual("1, 2, and 3", result)

    def test_convert_list_with_length_0_to_string(self):
        result: str = convert_list_to_string([])
        self.assertEqual("", result)

    def test_convert_list_with_str_elements_to_string(self):
        result: str = convert_list_to_string(["kind", "happy", "cool"])
        self.assertEqual("kind, happy, and cool", result)

    def test_convert_list_with_multiple_elements_types_to_string(self):
        result: str = convert_list_to_string(["kind", 1, True])
        self.assertEqual("kind, 1, and True", result)
