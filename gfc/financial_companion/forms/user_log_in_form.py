from django import forms


class UserLogInForm(forms.Form):
    """Form enabling signed-up users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
