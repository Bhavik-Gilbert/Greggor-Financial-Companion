from django import forms
from financial_companion.models import UserGroup
from financial_companion.helpers.functions import get_random_invite_code
from typing import Any


class UserGroupForm(forms.ModelForm):
    """Form to create user groups"""

    class Meta:
        model: UserGroup = UserGroup
        fields: list[str] = [
            'name',
            'description',
            'group_picture']
        widgets: dict[str: Any] = {'description': forms.Textarea()}

    def get_invite_code(self) -> str:
        generated_invite_code = get_random_invite_code(8)
        try:
            user_group: UserGroup = UserGroup.objects.get(
                invite_code=generated_invite_code)
        except UserGroup.DoesNotExist:
            return generated_invite_code
        self.get_invite_code()

    def save(self, current_user, instance=None) -> UserGroup:
        """Create a new user group."""

        super().save(commit=False)

        if instance is None:
            user_group: UserGroup = UserGroup.objects.create(
                name=self.cleaned_data.get('name'),
                description=self.cleaned_data.get('description'),
                owner_email=current_user.email,
                invite_code=self.get_invite_code(),
                group_picture=self.cleaned_data.get('group_picture'),
            )
        else:
            user_group = super().save()
        return user_group
