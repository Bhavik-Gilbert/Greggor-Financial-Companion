from .test_helper_base import HelperTestCase
from financial_companion.helpers import CurrencyType, CurrencyConversion, StoredCurrencyConverter
from typing import Any
from datetime import datetime

class CurrencyConversionHelperClassTestCase(HelperTestCase):
    """Test file for the CurrencyConversion helpers class"""

    def setUp(self) -> None:
        super().setUp()
        self.conversion: CurrencyConversion = CurrencyConversion(CurrencyType.USD, CurrencyType.GBP, 0.1, datetime.now())

    def test_valid_can_convert(self) -> None:
        self.assertTrue(self.conversion.can_convert(CurrencyType.USD, CurrencyType.GBP))

    def test_invalid_can_convert(self) -> None:
        self.assertFalse(self.conversion.can_convert(CurrencyType.CAD, CurrencyType.GBP))
        self.assertFalse(self.conversion.can_convert(CurrencyType.CAD, CurrencyType.USD))
        self.assertFalse(self.conversion.can_convert(CurrencyType.GBP, CurrencyType.CAD))
        self.assertFalse(self.conversion.can_convert(CurrencyType.USD, CurrencyType.CAD))

    def test_valid_conversion_in_date(self) -> None:
        self.assertTrue(self.conversion.conversion_in_date())
    
    def test_invalid_conversion_in_date(self) -> None:
        self.conversion.time_recorded = datetime(2024,2,16,0,0)
        self.assertFalse(self.conversion.conversion_in_date())
    
    def test_invalid_convert(self) -> None:
        self.assertEqual(self.conversion.convert(1, CurrencyType.CAD, CurrencyType.GBP), 1)
        self.assertEqual(self.conversion.convert(1, CurrencyType.CAD, CurrencyType.USD), 1)
        self.assertEqual(self.conversion.convert(1, CurrencyType.GBP, CurrencyType.CAD), 1)
        self.assertEqual(self.conversion.convert(1, CurrencyType.USD, CurrencyType.CAD), 1)

    def test_original_direction_convert(self) -> None:
        self.assertEqual(0.1, self.conversion.convert(1, CurrencyType.USD, CurrencyType.GBP))

    def test_original_direction_convert(self) -> None:
        self.assertEqual(10, self.conversion.convert(1, CurrencyType.GBP, CurrencyType.USD))
    
class StoredCurrencyConverterHelperClassTestCase(HelperTestCase):
    """Test file for the StoredCurrencyConverter helpers class"""
    def setUp(self) -> None:
        super().setUp()
        self.conversion: CurrencyConversion = CurrencyConversion(CurrencyType.USD, CurrencyType.GBP, 0.1, datetime.now())
        self.converter = StoredCurrencyConverter() 
        self.converter.conversion_list.append(self.conversion)
    
    def test_valid_has_valid_conversion(self) -> None:
        self.assertTrue(self.converter.has_valid_conversion(CurrencyType.USD, CurrencyType.GBP))
        self.assertTrue(self.converter.has_valid_conversion(CurrencyType.GBP, CurrencyType.USD))
    
    def test_invalid_has_valid_conversion(self) -> None:
        self.assertFalse(self.converter.has_valid_conversion(CurrencyType.USD, CurrencyType.CAD))
        self.assertFalse(self.converter.has_valid_conversion(CurrencyType.CAD, CurrencyType.GBP))
    
    def test_invalid_get_conversion(self) -> None:
        self.assertTrue(self.converter.get_conversion(CurrencyType.USD, CurrencyType.CAD) is None)
        self.assertTrue(self.converter.get_conversion(CurrencyType.CAD, CurrencyType.GBP) is None)

    def test_valid_get_conversion(self) -> None:
        self.assertEqual(self.conversion, self.converter.get_conversion(CurrencyType.USD, CurrencyType.GBP))
        self.assertEqual(self.conversion, self.converter.get_conversion(CurrencyType.GBP, CurrencyType.USD))
    
    def test_add_conversion(self) -> None:
        self.assertEqual(1, len(self.converter.conversion_list))
        self.converter.add_conversion(CurrencyType.USD, CurrencyType.GBP, 0.1)
        self.assertEqual(1, len(self.converter.conversion_list))
        self.converter.add_conversion(CurrencyType.GBP, CurrencyType.USD, 10)
        self.assertEqual(1, len(self.converter.conversion_list))
        self.converter.add_conversion(CurrencyType.CAD, CurrencyType.USD, 10)
        self.assertEqual(2, len(self.converter.conversion_list))

