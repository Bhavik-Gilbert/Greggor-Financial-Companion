from django import forms
from financial_companion.models import Category, CategoryTarget
from ..helpers import Timespan
from django.core.exceptions import ValidationError

class CreateCategoryForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Category
        fields = ['name', 'description']
    
    timespan = forms.ChoiceField(choices = [('','---------')] + Timespan.choices, required=False)
    amount = forms.DecimalField(decimal_places=2, max_digits=15, required = True, initial = 0, label = "Spending Limit")


    def save(self, current_user):
        """Create a new category."""
        super().save(commit=False)
        category = Category.objects.create(
            user = current_user,
            name=self.cleaned_data.get('name'),
            description=self.cleaned_data.get('description')
        )
        """Create a new category target if time span was specified."""
        if self.cleaned_data.get('time_span') != '':
            categoryTarget = CategoryTarget.objects.create(
            category_id = category,
            amount = self.cleaned_data.get('amount') ,
            timespan=self.cleaned_data.get('timespan')
        )
        return category