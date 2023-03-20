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

    def generate_invite_code(self) -> str:
        while True:
            generated_invite_code: str = get_random_invite_code(8)
            user_group_count: int = UserGroup.objects.filter(
                invite_code=generated_invite_code).count()

            if user_group_count == 0:
                return generated_invite_code

    def save(self, current_user, instance=None) -> UserGroup:
        """Create a new user group."""

        super().save(commit=False)

        if instance is None:
            user_group: UserGroup = UserGroup.objects.create(
                name=self.cleaned_data.get('name'),
                description=self.cleaned_data.get('description'),
                owner_email=current_user.email,
                invite_code=self.generate_invite_code(),
                group_picture=self.cleaned_data.get('group_picture'),
            )
        else:
            user_group = super().save()
        return user_group
