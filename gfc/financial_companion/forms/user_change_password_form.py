from django import forms
from django.core.validators import RegexValidator

class UserChangePasswordForm(forms.Form):
    """Form for users to change their password"""

    password = forms.CharField(label="Current Password", widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
