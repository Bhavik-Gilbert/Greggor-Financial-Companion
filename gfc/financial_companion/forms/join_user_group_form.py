from django import forms

class JoinUserGroupForm(forms.Form):
    """Form enabling logged in users to join user groups."""

    invite_code = forms.CharField(label="",max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Enter Group Invite Code', 'class': 'form-control'}))