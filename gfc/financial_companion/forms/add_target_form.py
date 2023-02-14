from django import forms
from financial_companion.models import CategoryTarget, Category
# from ..helpers import Timespan


class CategoryTargetForm(forms.ModelForm):
    """Form to add a target"""

    class Meta:
        model = CategoryTarget
        fields = ['transaction_type', 'timespan', 'amount','currency']


    def save(self, current_category: Category, instance: CategoryTarget = None)-> CategoryTarget:
        """Create a new target."""
        super().save(commit=False)
        if instance is None:
            print("ASFASFASFFFFFFF")
            print(current_category)
            category_target= CategoryTarget.objects.create(
                category=current_category,
                transaction_type=self.cleaned_data.get('transaction_type'),
                timespan=self.cleaned_data.get('timespan'),
                amount=self.cleaned_data.get('amount'),
                currency=self.cleaned_data.get('currency')

            )
        else:
            category_target: CategoryTarget = instance
            category_target.transaction_type = self.cleaned_data.get('transaction_type')
            category_target.timespan = self.cleaned_data.get('timespan')
            category_target.amount = self.cleaned_data.get('amount')
            category_target.currency = self.cleaned_data.get('currency')
            category_target.save()

        return category_target
