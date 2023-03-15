from .test_template_tag_base import TemplateTagTestCase
from financial_companion.helpers import GreggorTypes
from financial_companion.templatetags import get_greggor
import os
from freezegun import freeze_time
import datetime


class GetGreggorTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor logo template tag"""

    def _get_filename(self, greggor_path):
        return greggor_path.split(os.sep)[-1].split(".")[0].split("-")[-1]

    def test_valid_function_returns_input_if_valid_greggor_type(self):
        for greggor_type in GreggorTypes:
            greggor_path: str = get_greggor(greggor_type.lower())
            self.assertEqual(
                greggor_type.lower(),
                self._get_filename(greggor_path))

    def test_valid_function_accepts_upper_case_for_greggor_type(self):
        greggor_input: str = GreggorTypes.NORMAL
        self.assertTrue(greggor_input in GreggorTypes)
        greggor_path: str = get_greggor(greggor_input.upper())
        self.assertEqual(greggor_input, self._get_filename(greggor_path))

    def test_valid_function_accepts_lower_case_for_greggor_type(self):
        greggor_input: str = GreggorTypes.NORMAL
        self.assertTrue(greggor_input in GreggorTypes)
        greggor_path: str = get_greggor(greggor_input.lower())
        self.assertEqual(greggor_input, self._get_filename(greggor_path))

    def test_invalid_function_does_not_return_input_if_input_not_greggor_type(
            self):
        greggor_input: str = "not a greggor"
        self.assertFalse(greggor_input in GreggorTypes)
        greggor_path: str = get_greggor(greggor_input)
        greggor_filename: str = self._get_filename(greggor_path)
        self.assertNotEqual(greggor_input, greggor_filename)
        self.assertTrue(greggor_filename in GreggorTypes)

    def test_valid_function_returns_a_valid_greggor_type_if_input_is_empty(
            self):
        greggor_path: str = get_greggor("")
        greggor_filename: str = self._get_filename(greggor_path)
        self.assertNotEqual(greggor_path, greggor_filename)
        self.assertTrue(greggor_filename in GreggorTypes)

    @freeze_time("2012-01-01 10:00:00")
    def test_valid_party_greggor_on_holidays_without_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 10, 0, 0))
        greggor_path: str = get_greggor()
        self.assertEqual("party", self._get_filename(greggor_path))

    @freeze_time("2012-01-01 10:00:00")
    def test_valid_not_party_greggor_on_holidays_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 10, 0, 0))
        greggor_input: str = "normal"
        greggor_path: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual("party", greggor_input)
        self.assertNotEqual("party", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 22:00:00")
    def test_valid_sad_greggor_at_10pm_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 22, 0, 0))
        greggor_path: str = get_greggor("not a greggor")
        self.assertEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_sad_greggor_at_4am_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_path: str = get_greggor("not a greggor")
        self.assertEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-1 22:00:00")
    def test_valid_not_sad_greggor_at_10pm_with_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 22, 0, 0))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-1 4:00:00")
    def test_valid_sad_greggor_at_4am_with_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 4, 0, 0))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 22:00:00")
    def test_valid_not_sad_greggor_at_10pm_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 22, 0, 0))
        greggor_input: str = "normal"
        greggor_path: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual("sad", greggor_input)
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_not_sad_greggor_at_4am_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_input: str = "normal"
        greggor_path: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual("sad", greggor_input)
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 21:59:59")
    def test_valid_not_sad_greggor_before_10pm(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 21, 59, 59))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_sad_greggor_after_4am(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("sad", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_normal_greggor_during_day_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_path: str = get_greggor("not a greggor")
        self.assertEqual("normal", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_not_normal_greggor_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_input: str = "sad"
        greggor_path: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual("normal", greggor_input)
        self.assertNotEqual("normal", self._get_filename(greggor_path))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_not_normal_greggor_at_night(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("normal", self._get_filename(greggor_path))

    @freeze_time("2012-01-1 4:00:01")
    def test_valid_not_normal_greggor_on_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 4, 0, 1))
        greggor_path: str = get_greggor("not a greggor")
        self.assertNotEqual("normal", self._get_filename(greggor_path))
