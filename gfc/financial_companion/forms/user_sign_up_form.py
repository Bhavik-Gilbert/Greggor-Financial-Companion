from django import forms
from django.core.validators import RegexValidator
from financial_companion.models import User


class UserSignUpForm(forms.ModelForm):
    """Form to register users"""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'profile_picture']
        widgets = {'bio': forms.Textarea()}

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error(
                'password_confirmation',
                'Confirmation does not match password.')

    def save(self, instance=None):
        """Create a new user."""

        super().save(commit=False)

        if instance is None:
            user = User.objects.create_user(
                self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                bio=self.cleaned_data.get('bio'),
                password=self.cleaned_data.get('new_password'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        else:
            user = instance
            user.username = self.cleaned_data.get('username'),
            user.first_name = self.cleaned_data.get('first_name'),
            user.last_name = self.cleaned_data.get('last_name'),
            user.email = self.cleaned_data.get('email'),
            user.bio = self.cleaned_data.get('bio'),
            # user.password=self.cleaned_data.get('new_password'),
            user.profile_picture = self.cleaned_data.get('profile_picture')
        return user
