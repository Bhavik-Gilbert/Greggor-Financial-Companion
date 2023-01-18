from django.db import connection
from django.db.models.base import ModelBase

from .test_model_base import ModelTestCase


class AbstractModelTestCase(ModelTestCase):
    """
    Base class for tests of abstract models. To use, subclass and specify
    the mixin class variable. A model using the mixin will be made
    available in self.test_model.
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName=methodName)
        self.mixin = None

    def setUp(self):
        super().setUp()
        # Create a dummy model which extends the mixin
        self.test_model = ModelBase('__TestModel__' + self.mixin.__name__, (self.mixin,), {'__module__': self.mixin.__module__})

        # Create the schema for our test model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.test_model)

    def tearDown(self):
        # Delete the schema for the test model
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.test_model)