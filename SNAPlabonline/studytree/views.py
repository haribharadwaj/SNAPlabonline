from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import (login_required,
    permission_required)
from .models import BaseNode, StudyRoot, TaskNode, BranchNode
from .lookups import create_study_slug, get_leaves
from .forms import AddTaskForm, AddBranchForm



# Initializing a study
class StudyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = StudyRoot
    fields = ['name', 'displayname', 'descr', 'end_url']
    success_url = 'study-viewedit'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.ROOT
        form.instance.slug = create_study_slug()
        return super().form_valid(form)


# For clarity, using not-totally-DRY views for adding tasks and branches below

# Add task to study
class AddTaskView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = TaskNode
    form_class = AddTaskForm
    success_url = 'study-viewedit'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.TASK
        pk_parent = self.request.kwargs['parentpk']
        form.instance.parent_node = BaseNode.objects.get(pk=pk_parent)
        # Tell parent node that this is the child node
        form.instance.parent_node.child_node = form.instance
        form.instance.parent_node.save()  #form_valid only saves form.instance
        return super().form_valid(form)

    def test_func(self):
        task_node = self.get_object()
        if self.request.user == task_node.experimenter:
            return True
        else:
            return False


class AddAltTaskView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = TaskNode
    form_class = AddTaskForm
    success_url = 'study-viewedit'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.TASK
        pk_parent = self.request.kwargs['parentpk']
        form.instance.parent_node = BaseNode.objects.get(pk=pk_parent)
        # Tell parent node that this is the alternate child node
        form.instance.parent_node.child_alternate = form.instance
        form.instance.parent_node.save()  #form_valid only saves form.instance
        return super().form_valid(form)

    def test_func(self):
        task_node = self.get_object()
        if self.request.user == task_node.experimenter:
            return True
        else:
            return False


# Add branch to study
class AddBranchView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = BranchNode
    form_class = AddBranchForm
    success_url = 'study-viewedit'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.FORK
        pk_parent = self.request.kwargs['parentpk']
        form.instance.parent_node = BaseNode.objects.get(pk=pk_parent)
        # Tell parent node that this is the child node
        form.instance.parent_node.child_node = form.instance
        form.instance.parent_node.save()  #form_valid only saves form.instance
        return super().form_valid(form)

    def test_func(self):
        task_node = self.get_object()
        if self.request.user == task_node.experimenter:
            return True
        else:
            return False


class AddAltBranchView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = TaskNode
    form_class = AddTaskForm
    success_url = 'study-viewedit'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.FORK
        pk_parent = self.request.kwargs['parentpk']
        form.instance.parent_node = BaseNode.objects.get(pk=pk_parent)
        # Tell parent node that this is the alternate child node
        form.instance.parent_node.child_alternate = form.instance
        form.instance.parent_node.save()  #form_valid only saves form.instance
        return super().form_valid(form)

    def test_func(self):
        task_node = self.get_object()
        if self.request.user == task_node.experimenter:
            return True
        else:
            return False


# Function-based views for study tree and subject view
def experimenter_view(request):
	pass


def subject_view(request):
	pass


def mystudies(request):
	pass

