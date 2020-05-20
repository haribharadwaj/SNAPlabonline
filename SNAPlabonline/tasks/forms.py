from django import forms
from .models import Task, Response

class TaskCreationForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['name', 'icon', 'trialinfo']


class ResponseForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['answer']

