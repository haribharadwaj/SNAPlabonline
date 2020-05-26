from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .forms import TaskCreationForm, ResponseForm
from .models import Response, Task
from .lookups import get_task_context

# Create your views here.

def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks' : tasks})


@login_required
@permission_required('tasks.add_task', raise_exception=PermissionDenied)
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, request.FILES)
        form.instance.experimenter = request.user
        if form.is_valid():
            form.save()
            taskname = form.cleaned_data.get('displayname')
            messages.success(request, f'{taskname} task created!')
            return redirect('tasks-home')
    else:
        form = TaskCreationForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def run_task(request, **kwargs):
    task_name = kwargs['taskname']
    trialnum = kwargs['trialnum']
    task = Task.objects.get(name=task_name)
    display_name = task.displayname
    taskcontext = get_task_context(task, trialnum, request.user)

    if taskcontext['done']:
        return render(request, 'tasks/task_done.html', {'taskcontext': taskcontext})

    if taskcontext['no_more_trials']:
        return render(request, 'tasks/bad_trialnum.html', {'taskcontext': taskcontext})

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        form.instance.subject = request.user
        form.instance.trialnum = trialnum
        form.instance.parent_task = task
        if form.instance.answer == taskcontext['answer']:
            form.instance.correct = True
        else:
            form.instance.correct = False

        if form.is_valid():
            form.save()
            taskname = form.cleaned_data.get('name')
            if taskcontext['feedback']:
                if form.instance.correct:
                    messages.success(request, f'You got trial {trialnum} of {display_name} right!')
                else:
                    messages.error(request, f'You did not get trial {trialnum} of {display_name} right!')

            return redirect('run-task', taskname=task_name, trialnum=trialnum + 1)
    else:
        form = ResponseForm()
        form.instance.trialnum = trialnum
        form.instance.subject = request.user
        form.instance.parent_task = task
    context = {'taskcontext': taskcontext, 'trialnum': trialnum, 'form': form}
    return render(request, 'tasks/response_form.html', {'trial': context})

