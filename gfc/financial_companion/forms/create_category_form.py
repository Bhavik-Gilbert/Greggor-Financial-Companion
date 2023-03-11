from django import forms
from financial_companion.models import Category
from ..helpers import Timespan
from typing import Any

class CategoryForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model: Category = Category
        fields: list[str] = ['name', 'description']
        widgets: dict[str, Any] = {'description': forms.Textarea()}

    def save(self, current_user, instance: Category = None) -> Category:
        """Create a new category."""
        super().save(commit=False)
        if instance is None:
            category: Category = Category.objects.create(
                user=current_user,
                name=self.cleaned_data.get('name'),
                description=self.cleaned_data.get('description')
            )
        else:
            category: Category = instance
            category.name: str = self.cleaned_data.get('name')
            category.description: str = self.cleaned_data.get('description')
            category.save()

        return category
