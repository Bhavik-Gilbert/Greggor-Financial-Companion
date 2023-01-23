from django.db import connection
from django.db.models.base import ModelBase
from django.db.utils import ProgrammingError

from .test_model_base import ModelTestCase


class AbstractModelTestCase(ModelTestCase):
    """
    Base class for tests of abstract models. To use, subclass and specify
    the mixin class variable. A model using the mixin will be made
    available in self.model.
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName=methodName)
        self.mixin: AbstractModelTestCase = None

    @classmethod
    def setUpClass(self) -> None:
        """
        Create temporary model for abstract models
        Abstract model from self.mixin is used, assign in subclass
        New model stored in self.model
        """

        # Create dummy model extending Base, a mixin, if we haven't already.
        if not hasattr(self, 'model'):
            self.model: ModelBase = ModelBase(
                self.mixin.__name__,
                ( self.mixin, ),
                { '__module__': self.mixin.__module__ }
            )

            # Create the schema for our base model. 
            # If a schema is already create then let's not create another one.
            try:
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(self.model)
                super(AbstractModelTestCase, self).setUpClass()
            except ProgrammingError:
                pass


    @classmethod
    def tearDownClass(self) -> None:
        try:
            super(AbstractModelTestCase, self).tearDownClass()
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(self.model)
        except ProgrammingError:
            pass