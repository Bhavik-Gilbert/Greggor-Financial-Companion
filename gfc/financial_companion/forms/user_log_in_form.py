from django import forms


class UserLogInForm(forms.Form):
    """Form enabling signed-up users to log in."""

    username: forms.CharField = forms.CharField(label="Username")
    password: forms.CharField = forms.CharField(
        label="Password", widget=forms.PasswordInput())
