from django.shortcuts import render
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied, ValidationError 
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import (login_required,
    permission_required)
from .models import BaseNode, StudyRoot, TaskNode, BranchNode
from .lookups import create_study_slug, get_leaves, get_studytree_context
from .forms import AddTaskForm, AddBranchForm



# Initializing a study
class StudyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = StudyRoot
    fields = ['name', 'displayname', 'descr', 'end_url']
    success_url = '/study/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.ROOT
        form.instance.parent_node = None
        form.instance.slug = create_study_slug()
        return super().form_valid(form)


# Initializing a study
class StudyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = StudyRoot
    success_url = '/study/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.experimenter:
            return True
        else:
            return False


# For clarity, using not-totally-DRY views for adding tasks and branches below
# Thus, a different view class for each node type with slight code variations

# Add task to study
class AddTaskView(LoginRequiredMixin, PermissionRequiredMixin,
    UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed, or adding to the wrong study'
    model = TaskNode
    form_class = AddTaskForm
    success_url = '/study/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.TASK
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
        except BaseNode.DoesNotExist:
            val_err = ValidationError('The parent node you are adding child to does not exist')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.child_node is not None:
            val_err = ValidationError('Parent already has a child')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        form.instance.parent_node = parent_node
        # Tell parent node that this is the child node
        form.save()  # Needed before assigning form.instance as foreign key
        form.instance.parent_node.child_node = form.instance
        form.instance.parent_node.save()
        # No need to call super().form_valid() as form already saved
        # Just redirect to success_url
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        try:
            parent_node = BaseNode.objects.get(pk=self.kwargs['parentpk'])
        except BaseNode.DoesNotExist:
            return False
        if self.request.user == parent_node.experimenter:
            return True
        else:
            return False

    def get_success_url(self):
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
            print(parent_node)
            while parent_node.node_type != BaseNode.ROOT:
                parent_node = parent_node.parent_node
            slug = parent_node.studyroot.slug
        except BaseNode.DoesNotExist:
            return self.success_url
        return reverse('study-viewedit', kwargs={'slug': slug})


class AddAltTaskView(LoginRequiredMixin, PermissionRequiredMixin,
    UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed, or adding to the wrong study'
    model = TaskNode
    form_class = AddTaskForm
    success_url = '/study/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.TASK
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
        except BaseNode.DoesNotExist:
            val_err = ValidationError('The parent node you are adding child to does not exist')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.node_type != BaseNode.FORK:
            val_err = ValidationError('You can only add alternate after branching')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.branchnode.child_alternate is not None:
            val_err = ValidationError('Parent already has an alternate child')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        form.instance.parent_node = parent_node
        # Tell parent node that this is the child node
        form.save()  # Needed before assigning form.instance as foreign key
        form.instance.parent_node.branchnode.child_alternate = form.instance
        form.instance.parent_node.branchnode.save()
        # No need to call super().form_valid() as form already saved
        # Just redirect to success_url
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        try:
            parent_node = BaseNode.objects.get(pk=self.kwargs['parentpk'])
        except BaseNode.DoesNotExist:
            return False
        if self.request.user == parent_node.experimenter:
            return True
        else:
            return False

    def get_success_url(self):
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
            print(parent_node)
            while parent_node.node_type != BaseNode.ROOT:
                parent_node = parent_node.parent_node
            slug = parent_node.studyroot.slug
        except BaseNode.DoesNotExist:
            return self.success_url
        return reverse('study-viewedit', kwargs={'slug': slug})


# Add branch to study
class AddBranchView(LoginRequiredMixin, PermissionRequiredMixin,
    UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed, or adding to the wrong study'
    model = BranchNode
    form_class = AddBranchForm
    success_url = '/study/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.FORK
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
        except BaseNode.DoesNotExist:
            val_err = ValidationError('The parent node you are adding child to does not exist')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.node_type == BaseNode.ROOT:
            val_err = ValidationError('You have to add a task first')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.child_node is not None:
            val_err = ValidationError('Parent already has a child')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        form.instance.parent_node = parent_node
        # Tell parent node that this is the child node
        form.save()  # Needed before assigning form.instance as foreign key
        form.instance.parent_node.child_node = form.instance
        form.instance.parent_node.save()
        # No need to call super().form_valid() as form already saved
        # Just redirect to success_url
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        try:
            parent_node = BaseNode.objects.get(pk=self.kwargs['parentpk'])
        except BaseNode.DoesNotExist:
            return False
        if self.request.user == parent_node.experimenter:
            return True
        else:
            return False

    def get_success_url(self):
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
            print(parent_node)
            while parent_node.node_type != BaseNode.ROOT:
                parent_node = parent_node.parent_node
            slug = parent_node.studyroot.slug
        except BaseNode.DoesNotExist:
            return self.success_url
        return reverse('study-viewedit', kwargs={'slug': slug})


class AddAltBranchView(LoginRequiredMixin, PermissionRequiredMixin,
    UserPassesTestMixin, CreateView):
    permission_required = 'studytree.add_studyroot'
    permission_denied_message = 'Experimenter credentials needed, or adding to the wrong study'
    model = BranchNode
    form_class = AddBranchForm
    success_url = '/study/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.node_type = BaseNode.FORK
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
        except BaseNode.DoesNotExist:
            val_err = ValidationError('The parent node you are adding child to does not exist')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.node_type == BaseNode.ROOT:
            val_err = ValidationError('You have to add a task first')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.node_type != BaseNode.FORK:
            val_err = ValidationError('You can only add alternate after branching')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        if parent_node.branchnode.child_alternate is not None:
            val_err = ValidationError('Parent already has an alternate child')
            form.add_error(None, val_err)  # Non-field error
            return super().form_invalid(form)
        form.instance.parent_node = parent_node
        # Tell parent node that this is the child node
        form.save()  # Needed before assigning form.instance as foreign key
        form.instance.parent_node.branchnode.child_alternate = form.instance
        form.instance.parent_node.branchnode.save()
        # No need to call super().form_valid() as form already saved
        # Just redirect to success_url
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        try:
            parent_node = BaseNode.objects.get(pk=self.kwargs['parentpk'])
        except BaseNode.DoesNotExist:
            return False
        if self.request.user == parent_node.experimenter:
            return True
        else:
            return False

    def get_success_url(self):
        pk_parent = self.kwargs['parentpk']
        try:
            parent_node = BaseNode.objects.get(pk=pk_parent)
            print(parent_node)
            while parent_node.node_type != BaseNode.ROOT:
                parent_node = parent_node.parent_node
            slug = parent_node.studyroot.slug
        except BaseNode.DoesNotExist:
            return self.success_url
        return reverse('study-viewedit', kwargs={'slug': slug})


class MyStudies(LoginRequiredMixin, ListView):
    template_name = 'studytree/study_list.html'
    def get_queryset(self):
        # Return only tasks of logged in experimenter from new to old
        return StudyRoot.objects.filter(experimenter=self.request.user).order_by('-date_created')



# Function-based views for study tree and subject detail views
@login_required
@permission_required('studytree.add_studyroot',
    raise_exception=PermissionDenied('Experimenter credentials needed to visit this page'))
def experimenter_view(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    if slug is None:
        raise Http404('You are requesting a null study')
    else:
        try:
            root_node = StudyRoot.objects.get(slug=slug)
        except StudyRoot.DoesNotExist:
            raise Http404('Study does not seem to exist')
        if root_node.experimenter == request.user:
            return render(request,'studytree/study_detail.html',
                {'treedict': get_studytree_context(root_node)})
        else:
            message = f'Does not seem to be your study: You are logged in as {request.user}.'
            raise PermissionDenied(message)            



# MAIN VIEW FOR SUBJECT
def subject_view(request, *args, **kwargs):
	raise Http404('We are still building that page for you!')



