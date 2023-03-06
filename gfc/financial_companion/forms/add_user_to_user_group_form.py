from django import forms


class AddUserToUserGroupForm(forms.Form):
    """Form enabling users to be added to user groups."""

    user_email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': "Enter User's Email",
                'class': 'form-control rounded'}))
