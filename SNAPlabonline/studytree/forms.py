from django.forms import ModelForm
from .models import TaskNode


class AddTaskForm(ModelForm):
	class Meta:
		model = TaskNode
		fields = ['task']  # Add queryset of current user!!