from django import forms
from .models import Task, Response

class TaskCreationForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['name', 'displayname', 'descr', 'icon', 'tasktype', 'trialinfo']


class ResponseForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['answer']

class TaskEditForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['displayname', 'descr', 'icon', 'trialinfo']
