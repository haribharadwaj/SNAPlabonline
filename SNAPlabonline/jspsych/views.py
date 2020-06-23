from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.decorators import (login_required,
    permission_required)
from django.core.exceptions import PermissionDenied
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from .models import (OneShotResponse, SingleTrialResponse,
    ConstStimTask)
from users.models import Subject
from .lookups import (get_task_context, create_task_slug,
    get_task_results)
from secrets import token_urlsafe
from users.decorators import subjid_required, consent_required
import json  # Needed to parse AJAX posts



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
        task = ConstStimTask.objects.get(task_url=task_url)
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
        task_url = request.POST['task_url']  # Retain as string
        task = ConstStimTask.objects.get(task_url=task_url)
        trialnum = json.loads(request.POST['trialnum'])  # Coerse to number
        correct = json.loads(request.POST['correct'])  # Coerse to boolean
        resp = SingleTrialResponse(data=dat,
            subject=subj,
            parent_task=task,
            trialnum=trialnum,
            correct=correct)
        resp.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



class ConstStimTaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'jspsych/task_form.html'
    permission_required = 'jspsych.add_jstask'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = ConstStimTask
    fields = ['name', 'displayname', 'descr', 'trialinfo']
    success_url = '/mytasks/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
        form.instance.task_url = create_task_slug()
        return super().form_valid(form)


class ConstStimTaskListView(LoginRequiredMixin, ListView):
    template_name = 'jspsych/task_list.html'
    def get_queryset(self):
        # Return only tasks of logged in experimenter from new to old
        return ConstStimTask.objects.filter(experimenter=self.request.user).order_by('-date_created')


class ConstStimTaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ConstStimTask
    template_name = 'jspsych/task_form.html'
    fields = ['name', 'displayname', 'descr', 'trialinfo']
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


class ConstStimTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ConstStimTask
    template_name = 'jspsych/task_confirm_delete.html'
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
        return render(request, 'jspsych/task_done.html',
            {'taskcontext': taskcontext})

    return render(request, 'jspsych/task_run.html',
        {'task': taskcontext})



@login_required
@permission_required('tasks.add_task', raise_exception=PermissionDenied)
def download_task_results(request, **kwargs):
    task_url = kwargs['taskurl']
    experimenter = request.user
    results_dict, filename = get_task_results(task_url, experimenter)

    if results_dict is not None:
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        json.dump(results_dict, response, indent=4, sort_keys=True)
        return response
    else:
        forbidden_message = ('Looks like you are requesting results for '
            'a task that you did not create ...')
        raise PermissionDenied(forbidden_message)


