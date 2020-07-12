from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied, ValidationError 
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import (login_required,
    permission_required)
from django.utils import timezone
from django.contrib import messages
from users.decorators import subjid_required, consent_required
from users.models import Subject
from .models import BaseNode, StudyRoot, TaskNode, BranchNode
from .lookups import (create_study_slug, get_studytree_context,
    get_next_task, get_max_tasks, get_info,
    create_demo_subject, create_pilot_subject)
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

    # Need to update kwargs passed to FormClass to have user
    # This is so form can filter queryset for ModelChoiceField
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddTaskView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

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

    # Need to update kwargs passed to FormClass to have user
    # This is so form can filter queryset for ModelChoiceField
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddAltTaskView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

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
@subjid_required
@consent_required
def subject_view(request, *args, **kwargs):
    studyslug = kwargs.get('slug', None)
    # Keep track of which one the subject is doing
    request.session['studyslug'] = studyslug  
    subjid = request.session.get('subjid')
    if studyslug is None:
        raise Http404('You are requesting a null study')
    else:
        if StudyRoot.objects.filter(slug=studyslug).exists():
            node = StudyRoot.objects.get(slug=studyslug)
            ntasks_max = get_max_tasks(node)
            task, taskcomp, n_completed, totalcomp = get_next_task(node,
                studyslug, subjid)
            if n_completed < ntasks_max:
                if task is None:
                    status = 'Concluded Early'
                else:
                    status = 'In Progress'
            else:
                status = 'Completed'
        else:
            raise Http404('Study does not seem to exist')

    isdemo = kwargs.get('isdemo', False)
    ispilot = kwargs.get('ispilot', False)
    if isdemo or ispilot:
        totalcomp = 0.00
        taskcomp = 0.00

    study = dict(displayname=node.studyroot.displayname,
        status=status, taskcomp=taskcomp,
        marketplace='Prolific', subjid=subjid, task=task,
        ntasks_max=ntasks_max, n_completed=n_completed,
        totalcomp=totalcomp, isdemo=isdemo, ispilot=ispilot)
    return render(request, 'studytree/study_subject.html', {'study': study})



def demo_view(request, *args, **kwargs):
    subjid = request.session.get('subjid', None)
    if subjid is None or not subjid.startswith('DEMO'):
        subjid = create_demo_subject()
        request.session['subjid'] = subjid
        request.session['isdemo'] = True
    subj, was_just_created = Subject.objects.get_or_create(subjid=subjid)
    subj.latest_visit = timezone.now()
    subj.save()
    if was_just_created:
        messages.success(request,
            f'Because this is a demo study, we generated a random ID for you: {subjid}')
    # Pass to regular subject view, with demo ID
    kwargs.update({'isdemo': True})
    return subject_view(request, *args, **kwargs)


def pilot_view(request, *args, **kwargs):
    subjid = request.session.get('subjid', None)
    if subjid is None or not subjid.startswith('PILOT'):
        subjid = create_pilot_subject()
        request.session['subjid'] = subjid
        request.session['ispilot'] = True
    subj, was_just_created = Subject.objects.get_or_create(subjid=subjid)
    subj.latest_visit = timezone.now()
    subj.save()
    if was_just_created:
        messages.success(request,
            f'Because this is a pilot study, we generated a random ID for you: {subjid}')
    # Pass to regular subject view, with demo ID
    kwargs.update({'ispilot': True})
    return subject_view(request, *args, **kwargs)


@subjid_required
def wrong_id(request, *args, **kwargs):
    studyslug = request.session.get('studyslug', None)
    if studyslug is None:
        next_url = request.META.get('HTTP_REFERER', None)
        if next_url is None:
            next_url = reverse('study-routingfail')
    else:
        next_url = reverse('study-run', kwargs={'slug': studyslug})

    request.session.flush()
    return redirect(next_url)


def routing_fail(request):
    return render(request, 'studytree/routing_fail.html')


def redirect_home(request):
    studyslug = request.session.get('studyslug', None)
    isdemo = request.session.get('isdemo', False)
    ispilot = request.session.get('ispilot', False)
    if studyslug is None:
        next_url = request.META.get('HTTP_REFERER', None)
        if next_url is None:
            next_url = reverse('study-routingfail')
    else:
        if isdemo:
            next_url = reverse('study-demo', kwargs={'slug': studyslug})
        elif ispilot:
            next_url = reverse('study-pilot', kwargs={'slug': studyslug})
        else:
            next_url = reverse('study-run', kwargs={'slug': studyslug})
    return redirect(next_url)
