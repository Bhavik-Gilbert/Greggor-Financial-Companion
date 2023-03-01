from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_number_of_completed_targets
from financial_companion.models import User


class GetNumberOfCompletedTaregtsHelperFunctionTestCase(HelperTestCase):
    """Test for the get_number_of_completed_targets helpers function"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.targets = self.user.get_all_targets()
