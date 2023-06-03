from django import forms
from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    town = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    class Meta:
        model = User
        fields = ('username', 'town', 'image')

