from django.test import TestCase
from django.conf import settings
import os
from django.core.files.uploadedfile import TemporaryUploadedFile


class BaseTestCase(TestCase):
    """
    Base class for testing.
    Setup universally used fixtures and information across tests
    """

    fixtures: list[str] = [
        "example_category.json",
        "example_transactions.json",
        "example_users.json",
        "example_accounts.json",
        "example_targets.json",
        "example_recurring_transaction.json",
        "example_user_groups.json",
        "example_link_recurring_transaction.json",
        "example_quiz.json",
    ]

    def setUp(self) -> None:
        super().setUp()

    def _get_upload_file(self, app_file_path) -> TemporaryUploadedFile:
        """
        Takes a local file and returns a copy of it that can be uploaded into a form
        USAGE
        local_file_path = financial_companion/tests/data/filepath
        """
        local_file_path: str = os.path.join(settings.BASE_DIR, app_file_path)
        self.assertTrue(os.path.exists(local_file_path))
        upload_file: TemporaryUploadedFile = None
        with open(local_file_path, 'rb') as local_file:
            file_name: str = local_file.name
            file_length: int = os.path.getsize(local_file_path)
            
            upload_file: TemporaryUploadedFile = TemporaryUploadedFile(file_name, "application/binary", file_length, 'utf-8')
            upload_file.file.write(local_file.read())
            upload_file.file.seek(0)

        return upload_file
