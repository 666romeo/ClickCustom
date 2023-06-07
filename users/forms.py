from django import forms
from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/jpeg, image/png'}), required=False)
    class Meta:
        model = User
        fields = ['image']

