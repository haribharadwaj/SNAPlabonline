from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.mixins import (LoginRequiredMixin,
    PermissionRequiredMixin, UserPassesTestMixin)
from django.views.generic import (ListView,
    CreateView, UpdateView, DeleteView)
from .models import (OneShotResponse, SingleTrialResponse,
	Jstask)


# Create your views here.

def testview(request):
    return render(request, 'jstask/test.html')


@ensure_csrf_cookie
def create_OneShotResponse(request):
    if request.is_ajax() and request.method == 'POST':
        dat = request.POST['jsPsychData']
        resp = OneShotResponse.objects.create(data=dat)
        resp.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@ensure_csrf_cookie
def create_TrialResponse(request):
    if request.is_ajax() and request.method == 'POST':
        dat = request.POST['jsPsychData']
        resp = SingleTrialResponse.objects.create(data=dat)
        resp.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



# Views for working with Jstask

class JstaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'tasks.add_task'
    permission_denied_message = 'Experimenter credentials needed to create tasks'
    model = Jstask
    fields = ['name', 'displayname', 'descr', 'icon', 'tasktype', 'trialinfo']
    success_url = '/mytasks/'

    def form_valid(self, form):
        form.instance.experimenter = self.request.user
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