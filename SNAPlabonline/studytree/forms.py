from django.forms import ModelForm
from .models import TaskNode, BranchNode


class AddTaskForm(ModelForm):
	class Meta:
		model = TaskNode
		fields = ['task']  # Add queryset of current user!!


class AddBranchForm(ModelForm):
	class Meta:
		model = BranchNode
		fields = ['check_type', 'threshold', 'condition']