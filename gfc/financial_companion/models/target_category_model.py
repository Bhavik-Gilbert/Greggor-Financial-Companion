from django.db.models import (
    ForeignKey,
    CASCADE
)

from .abstract_target_model import AbstractTarget
from .category_model import Category

class TargetCategory(AbstractTarget):
    """Model for target spending and saving on categories"""

    category_id: ForeignKey = ForeignKey(Category, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "category_id"]