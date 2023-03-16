from typing import Any
from .test_helper_base import HelperTestCase
from financial_companion.helpers import paginate
import random
from django.core.paginator import Page

class PaginateFunctionTestCase(HelperTestCase):
    """Test file for the paginate helpers function"""

    def setUp(self):
        self.random_list: list[int] = []
        for i in range(0, 15):
            n: int  = random.randint(1, 30)
            self.random_list.append(n)

    def test_valid_page_number_given(self):
        list_of_items: Page = paginate(1, self.random_list)
        self.assertEqual(list_of_items.object_list, self.random_list[:10])

    def test_last_page_number_given(self):
        list_of_items: Page = paginate(2, self.random_list)
        self.assertEqual(list_of_items.object_list, self.random_list[-5:])

    def test_invalid_page_number_given(self):
        list_of_items: Page = paginate(12, self.random_list)
        self.assertEqual(list_of_items.object_list, self.random_list[-5:])

    def test_empty_list_given(self):
        self.random_list: list[Any] = []
        list_of_items: Page = paginate(2, self.random_list)
        self.assertEqual(list_of_items.object_list, [])

    def test_non_integer_page_number_given(self):
        list_of_items: Page = paginate("string", self.random_list)
        self.assertEqual(list_of_items.object_list, self.random_list[:10])
