from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import (login_required,
    permission_required)
from .models import StudyRoot, TaskNode, BranchNode, LeafNode
from .lookups import create_study_slug, get_current_leaf
from .forms import AddTaskForm



# Initializing a study
class StudyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = StudyRoot
    fields = ['name', 'displayname', 'descr', 'end_url']
    success_url = 'study-create'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.slug = create_study_slug()
        return super().form_valid(form)


# Add task to study
class AddTaskView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = TaskNode
    form_class = AddTaskForm
    success_url = 'study-create'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        root_node = StudyRoot.objects.get(slug=self.kwargs['studyslug'])
        form.instance.parent_node = get_current_leaf(root_node)
        return super().form_valid(form)

    def test_func(self):
        task_node = self.get_object()
        if self.request.user == task_node.experimenter:
            return True
        else:
            return False