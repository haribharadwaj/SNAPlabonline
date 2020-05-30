from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .forms import TaskCreationForm, ResponseForm
from .models import Response, Task
from .lookups import user_next_trial

# Create your views here.

def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks' : tasks})

def for_lab_members(request):
    return render(request, 'tasks/labmembers.html')

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

    taskcontext = user_next_trial(task_name, request.user)

    if taskcontext['done']:
        return render(request, 'tasks/task_done.html', {'taskcontext': taskcontext})

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        form.instance.subject = request.user
        form.instance.trialnum = taskcontext['trialnum']
        form.instance.parent_task_id = task_name

        if int(request.POST['answer']) == taskcontext['answer']:
            form.instance.correct = True
        else:
            form.instance.correct = False

        if form.is_valid():
            form.save()
            if taskcontext['feedback']:
                trialnum = taskcontext['trialnum']
                display_name = taskcontext['display_name']
                if form.instance.correct:
                    messages.success(request, f'You got trial {trialnum} of {display_name} right')
                else:
                    messages.warning(request, f'You did not get trial {trialnum} of {display_name} right!')

            return redirect('run-task', taskname=task_name)
    else:
        form = ResponseForm()
        form.instance.trialnum = taskcontext['trialnum']
        form.instance.subject = request.user
        form.instance.parent_task_id = task_name

    context = {'taskcontext': taskcontext, 'form': form}
    return render(request, 'tasks/response_form.html', {'trial': context})

