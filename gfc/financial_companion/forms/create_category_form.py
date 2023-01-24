from django import forms
from financial_companion.models import Category

class CreateCategoryForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Category
        fields = ['name', 'description']

    def save(self, current_user):
        """Create a new transaction."""

        super().save(commit=False)
        category = Category.objects.create(
            user = current_user,
            name=self.cleaned_data.get('name'),
            description=self.cleaned_data.get('description')
        )
        return category