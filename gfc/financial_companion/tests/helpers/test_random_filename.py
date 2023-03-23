from .test_helper_base import HelperTestCase
from financial_companion.helpers import random_filename
import datetime
from freezegun import freeze_time


class RandomFilenameHelperFunctionTestCase(HelperTestCase):
    """Test file for the random_filename helpers function"""

    def setUp(self):
        super().setUp()
        self.filename: str = "greggor.png"

    def test_get_correct_file_extension(self):
        filename: str = random_filename(self.filename)
        self.assertEqual(self.filename.split(".")[-1], filename.split(".")[-1])

    @freeze_time("2012-01-14 22:00:00")
    def test_valid_random_filename_contains_current_datetime(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 22, 0, 0))
        filename: str = random_filename(self.filename)
        self.assertTrue(str(datetime.datetime.now()) in filename)
