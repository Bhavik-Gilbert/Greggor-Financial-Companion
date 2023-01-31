from django import forms
from ..models.user_model import User

class EditUserDetailsForm(forms.ModelForm):
    "Form to edit a user's details"
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'profile_picture']
        widgets = { 'bio': forms.Textarea() }
