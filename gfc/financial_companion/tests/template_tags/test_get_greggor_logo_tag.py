from .test_template_tag_base import TemplateTagTestCase
from financial_companion.helpers import GreggorTypes
from financial_companion.templatetags import get_greggor
import os
from freezegun import freeze_time
import datetime


class GetGreggorTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor logo template tag"""

    def _get_name_in_filename(self, greggor_filename: str) -> str:
        """Returns greggor name within filename"""
        return greggor_filename.split(os.sep)[-1].split(".")[0].split("-")[-1]

    def test_valid_function_returns_input_if_valid_greggor_type(self):
        for greggor_type in GreggorTypes:
            greggor_filename: str = get_greggor(greggor_type.lower())
            self.assertEqual(
                greggor_type.lower(),
                self._get_name_in_filename(greggor_filename))

    def test_valid_function_accepts_upper_case_for_greggor_type(self):
        greggor_input: str = GreggorTypes.NORMAL
        self.assertTrue(greggor_input in GreggorTypes)
        greggor_filename: str = get_greggor(greggor_input.upper())
        self.assertEqual(
            greggor_input,
            self._get_name_in_filename(greggor_filename))

    def test_valid_function_accepts_lower_case_for_greggor_type(self):
        greggor_input: str = GreggorTypes.NORMAL
        self.assertTrue(greggor_input in GreggorTypes)
        greggor_filename: str = get_greggor(greggor_input.lower())
        self.assertEqual(
            greggor_input,
            self._get_name_in_filename(greggor_filename))

    def test_invalid_function_does_not_return_input_if_input_not_greggor_type(
            self):
        greggor_input: str = "not a greggor"
        self.assertFalse(greggor_input in GreggorTypes)
        greggor_filename: str = get_greggor(greggor_input)
        greggor_name: str = self._get_name_in_filename(greggor_filename)
        self.assertNotEqual(greggor_input, greggor_name)
        self.assertTrue(greggor_name in GreggorTypes)

    def test_valid_function_returns_a_valid_greggor_type_if_input_is_empty(
            self):
        greggor_filename: str = get_greggor("")
        greggor_name: str = self._get_name_in_filename(greggor_filename)
        self.assertNotEqual(greggor_filename, greggor_name)
        self.assertTrue(greggor_name in GreggorTypes)

    @freeze_time("2012-01-01 10:00:00")
    def test_valid_party_greggor_on_holidays_without_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 10, 0, 0))
        greggor_filename: str = get_greggor()
        self.assertEqual(
            GreggorTypes.PARTY,
            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-01 10:00:00")
    def test_valid_not_party_greggor_on_holidays_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 10, 0, 0))
        greggor_input: str = GreggorTypes.NORMAL
        greggor_filename: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual(GreggorTypes.PARTY, greggor_input)
        self.assertNotEqual(
            GreggorTypes.PARTY,
            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 22:00:00")
    def test_valid_sleepy_greggor_at_10pm_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 22, 0, 0))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertEqual(GreggorTypes.SLEEPY,
                         self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_sleepy_greggor_at_4am_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertEqual(GreggorTypes.SLEEPY,
                         self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-1 22:00:00")
    def test_valid_not_sleepy_greggor_at_10pm_with_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 22, 0, 0))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(
            GreggorTypes.SLEEPY,
            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-1 4:00:00")
    def test_valid_sad_greggor_at_4am_with_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 4, 0, 0))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(GreggorTypes.SAD,
                            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 22:00:00")
    def test_valid_not_sad_greggor_at_10pm_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 22, 0, 0))
        greggor_input: str = GreggorTypes.NORMAL
        greggor_filename: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual(GreggorTypes.SAD, greggor_input)
        self.assertNotEqual(GreggorTypes.SAD,
                            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_not_sad_greggor_at_4am_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_input: str = GreggorTypes.NORMAL
        greggor_filename: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual(GreggorTypes.SAD, greggor_input)
        self.assertNotEqual(GreggorTypes.SAD,
                            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 21:59:59")
    def test_valid_not_sad_greggor_before_10pm(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 21, 59, 59))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(GreggorTypes.SAD,
                            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_sad_greggor_after_4am(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(GreggorTypes.SAD,
                            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_normal_greggor_during_day_without_valid_input_and_not_holiday(
            self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertEqual(GreggorTypes.NORMAL,
                         self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:01")
    def test_valid_not_normal_greggor_with_valid_input(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 1))
        greggor_input: str = GreggorTypes.SAD
        greggor_filename: str = get_greggor(greggor_input)
        self.assertTrue(greggor_input in GreggorTypes)
        self.assertNotEqual(GreggorTypes.NORMAL, greggor_input)
        self.assertNotEqual(
            GreggorTypes.NORMAL,
            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-14 4:00:00")
    def test_valid_not_normal_greggor_at_night(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 14, 4, 0, 0))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(
            GreggorTypes.NORMAL,
            self._get_name_in_filename(greggor_filename))

    @freeze_time("2012-01-1 4:00:01")
    def test_valid_not_normal_greggor_on_holiday(self):
        self.assertEqual(
            datetime.datetime.now(), datetime.datetime(
                2012, 1, 1, 4, 0, 1))
        greggor_filename: str = get_greggor("not a greggor")
        self.assertNotEqual(
            GreggorTypes.NORMAL,
            self._get_name_in_filename(greggor_filename))
