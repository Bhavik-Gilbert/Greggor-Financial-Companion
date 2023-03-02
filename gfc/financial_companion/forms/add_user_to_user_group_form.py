from django import forms


class AddUserToUserGroupForm(forms.Form):
    """Form enabling users to be added to user groups."""

    user_email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': "Enter User's Email",
                'class': 'form-control rounded'}))