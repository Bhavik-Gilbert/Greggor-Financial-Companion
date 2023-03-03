from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_projection_timescale_options


class GetProjectionTimescaleOptionsHelperFunctionTestCase(HelperTestCase):
    """Test for the get_projection_timescale_options helpers function"""

    def test_return_valid_timescale_options(self):
        projectionTimescaleOptions = get_projection_timescale_options()
        self.assertGreater(len([*projectionTimescaleOptions]), 0)
        for months, displayString in projectionTimescaleOptions.items():
            self.assertIsInstance(months, int)
            self.assertGreater(months, 0)
            self.assertIsInstance(displayString, str)
            self.assertGreater(len(displayString), 0)
