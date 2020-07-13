from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SubjectProfile
from django.core.exceptions import ValidationError



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Not using model forms so that we can get_or_create() Subject objects:
# get_or_create() is messy to do with ModelForm.save() because
# uniqueness IntegrityErrors might arise in form.is_valid()
class SubjectForm(forms.Form):
    subjid = forms.CharField(max_length=32, label='Participant ID',
        help_text='Please enter or confirm your ID one more time')


class ConsentForm(forms.Form):
    consented = forms.BooleanField(required=True,
        label='I understand the information presented here and am OK to proceed')


class SubjectProfileForm(forms.ModelForm):
    class Meta:
        model = SubjectProfile
        exclude = ['subject', ]

    def clean_age(self):
        age = self.cleaned_data.get('age')
        message = 'Age of 18+ is needed for participation'
        code = 'invalid'
        if age < 18:
            raise ValidationError(message=message, code=code)
        return age


