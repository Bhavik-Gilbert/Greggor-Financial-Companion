from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_projection_timescale_options


class GetProjectionTimescaleOptionsHelperFunctionTestCase(HelperTestCase):
    """Test file for the get_projection_timescale_options helpers function"""

    def test_return_valid_timescale_options(self):
        projection_timescale_options: dict[int,
                                         str] = get_projection_timescale_options()
        self.assertGreater(len([*projection_timescale_options]), 0)
        for months, display_string in projection_timescale_options.items():
            self.assertIsInstance(months, int)
            self.assertGreater(months, 0)
            self.assertIsInstance(display_string, str)
            self.assertGreater(len(display_string), 0)
