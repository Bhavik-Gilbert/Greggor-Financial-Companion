from .test_helper_base import HelperTestCase
from financial_companion.helpers import random_filename
from datetime import datetime

class RandomFilenameHelperFunctionTestCase(HelperTestCase):
    """Test for the random_filename helpers function"""

    def setUp(self):
        self.filename = "greggor.png"
    
    def test_get_correct_file_extension(self):
        filename: str = random_filename(self.filename)
        self.assertEqual(self.filename.split(".")[-1], filename.split(".")[-1])

    def test_valid_random_filename_contains_current_datetime(self):
        filename: str = random_filename(self.filename)
        self.assertTrue(str(datetime.now()) in filename)
