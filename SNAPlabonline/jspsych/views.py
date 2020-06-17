from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from .models import (OneShotResponse, SingleTrialResponse,
    Jstask)
from users.models import Subject
from .lookups import get_task_context, create_task_slug
from secrets import token_urlsafe
from users.decorators import subjid_required, consent_required


# Create your views here.

def testview(request):
    return render(request, 'jstask/test.html')


# Views for responding to AJAX requests from jsPsych
@ensure_csrf_cookie
def create_OneShotResponse(request):
    if request.is_ajax() and request.method == 'POST':
        dat = request.POST['jsPsychData']
        subjid = request.POST['subjid']
        subj = Subject.objects.get(subjid=subjid)
        task_url = request.POST['task_url']
        task = Jstask.objects.get(task_url=task_url)
        interactions = request.POST['interactionData']
        resp = OneShotResponse(data=dat,
            subject=subj,
            parent_task=task,
            interactions=interactions)
        resp.save()
        json_resp = {'success': True, 
        'message': f'The data for {subjid} was saved'}
        return JsonResponse(json_resp)
    else:
        return JsonResponse({'success': False,
            'message': 'Sorry! Only POSTs can save data'})


@ensure_csrf_cookie
def create_TrialResponse(request):
    if request.is_ajax() and request.method == 'POST':
        dat = request.POST['jsPsychData']
        subjid = request.POST['subjid']
        subj = Subject.objects.get(subjid=subjid)
        task_url = request.POST['task_url']
        task = Jstask.objects.get(task_url=task_url)
        trialnum = request.POST['trialnum']
        resp = SingleTrialResponse(data=dat,
            subject=subj,
            parent_task=task,
            trialnum=trialnum)
        resp.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



class JstaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'jspsych.add_jstask'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = Jstask
    fields = ['name', 'displayname', 'descr', 'icon', 'tasktype', 'trialinfo']
    success_url = '/mytasks/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.task_url = create_task_slug()
        return super().form_valid(form)


class JstaskListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        # Return only tasks of logged in experimenter from new to old
        return Jstask.objects.filter(experimenter=self.request.user).order_by('-date_created')


class JstaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jstask
    fields = ['name', 'displayname', 'descr', 'icon', 'trialinfo']
    success_url = '/mytasks/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.experimenter:
            return True
        else:
            return False


class JstaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Jstask
    success_url = '/mytasks/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.experimenter:
            return True
        else:
            return False


@subjid_required
@consent_required
def run_task(request, **kwargs):
    task_url = kwargs['taskurl']
    subject = request.session['subjid']


    # Gets the info for where the subject left off
    taskcontext = get_task_context(task_url, subject)    

    if taskcontext['done']:
        return render(request, 'tasks/task_done.html', {'taskcontext': taskcontext})

    return render(request, 'jspsych/jstask_run.html', {'task': taskcontext})
