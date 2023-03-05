from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_warning_messages_for_targets
from financial_companion.models import User
from django.http import HttpRequest
from django.contrib.messages import get_messages

class GetWarningMessagesForTargetsHelperFunctionTestCase(HelperTestCase):
    """Test for the get_warning_messages_for_targets helpers function"""

    def setUp(self):
        self.request = self.client.get('dashboard').wsgi_request
        self.request.user = User.objects.get(pk=1)
        self.targets = self.request.user.get_all_targets()

    def test_get_messages_no_show_numbers_no_targets(self):
        outputRequest: HttpRequest = get_warning_messages_for_targets(self.request)
        self._assert_request_as_valid(outputRequest)
    
    def test_get_messages_valid_show_numbers_no_targets(self):
        outputRequest: HttpRequest = get_warning_messages_for_targets(self.request)
        self._assert_request_as_valid(outputRequest)
    
    def test_get_messages_valid_show_numbers_null_targets(self):
        outputRequest: HttpRequest = get_warning_messages_for_targets(self.request, False, [])
        self._assert_request_as_valid(outputRequest)
    
    def test_get_messages_valid_show_numbers_valid_targets(self):
        outputRequest: HttpRequest = get_warning_messages_for_targets(self.request, True, self.targets)
        self._assert_request_as_valid(outputRequest)
    
    def _assert_request_as_valid(self, request: HttpRequest):
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertTrue('Targets exceeded: ' in str(messages[0]))