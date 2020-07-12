from django.forms import ModelForm, ModelChoiceField
from .models import TaskNode, BranchNode
from jspsych.models import Task


class AddTaskForm(ModelForm):
	class Meta:
		model = TaskNode
		fields = ['task', 'pay']  # Add queryset of current user!!

	# Need to override __init__ to only allow tasks created by user
	def __init__(self, *args, **kwargs):
		# need to use pop instead because
		# super().__init__ won't expect user key in kwargs
		user = kwargs.pop('user', None)
		super(AddTaskForm, self).__init__(*args, **kwargs)
		qs = (Task.objects.filter(experimenter=user) |
			Task.objects.filter(experimenter__username='coreuser'))
		self.fields['task'].queryset = qs


class AddBranchForm(ModelForm):
	class Meta:
		model = BranchNode
		fields = ['check_type', 'threshold', 'condition']