from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_warning_messages_for_targets
from financial_companion.models import User, AbstractTarget
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.contrib.messages.storage.base import Message
from freezegun import freeze_time


class GetWarningMessagesForTargetsHelperFunctionTestCase(HelperTestCase):
    """Test file for the get_warning_messages_for_targets helpers function"""

    @freeze_time("2023-01-05 13:00:00")
    def setUp(self):
        self.request: HttpRequest = self.client.get('dashboard').wsgi_request
        self.request.user: User = User.objects.get(pk=1)
        self.targets: list[AbstractTarget] = self.request.user.get_all_targets()

    @freeze_time("2023-01-05 13:00:00")
    def test_get_messages_no_show_numbers_no_targets(self):
        output_request: HttpRequest = get_warning_messages_for_targets(
            self.request)
        self._assert_message_request_as_valid(output_request)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_messages_valid_show_numbers_no_targets(self):
        output_request: HttpRequest = get_warning_messages_for_targets(
            self.request)
        self._assert_message_request_as_valid(output_request)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_messages_valid_show_numbers_null_targets(self):
        output_request: HttpRequest = get_warning_messages_for_targets(
            self.request, False, [])
        self._assert_message_request_as_valid(output_request)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_messages_valid_show_numbers_valid_targets(self):
        output_request: HttpRequest = get_warning_messages_for_targets(
            self.request, True, self.targets)
        self._assert_message_request_as_valid(output_request)

    @freeze_time("2023-01-05 13:00:00")
    def _assert_message_request_as_valid(self, request: HttpRequest):
        """Assert messages are in request"""
        messages: list[Message] = list(get_messages(request))
        self.assertEqual(len(messages), 3)
        self.assertLessEqual(len(messages), 3)
        self.assertTrue('Targets completed: ' in str(messages[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages[1]))
        self.assertTrue('Targets exceeded: ' in str(messages[2]))
