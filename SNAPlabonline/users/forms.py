from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
        	'username': _('MTurk ID or Username'),
        }
        help_texts = {
        	'username': _('Register with your MTurk ID if you have one, or create a new username'),
        	# Original: 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        }