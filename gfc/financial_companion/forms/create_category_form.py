from django import forms
from financial_companion.models import Category
from ..helpers import Timespan


class CategoryForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Category
        fields = ['name', 'description']
    

    def save(self, current_user, instance: Category = None) -> Category:
        """Create a new category."""
        super().save(commit=False)
        if instance is None:
            category = Category.objects.create(
                user = current_user,
                name=self.cleaned_data.get('name'),
                description=self.cleaned_data.get('description')
            )
        else:
             category: Category = instance
             category.name  = self.cleaned_data.get('name')
             category.description = self.cleaned_data.get('description')
             category.save()

        return category