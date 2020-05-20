import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskCreationForm, ResponseForm
from .models import Response, Task

# Create your views here.

def index(request):
    return render(request, 'tasks/home.html')

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, request.FILES)
        form.instance.experimenter = request.user
        if form.is_valid():
            form.save()
            taskname = form.cleaned_data.get('name')
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
    taskcontext = get_task_context(task, trialnum)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        form.instance.subject = request.user
        form.instance.trialnum = trialnum
        form.instance.parent_task = task
        if form.is_valid():
            form.save()
            taskname = form.cleaned_data.get('name')
            messages.success(request, f'Trial {trialnum} of {task_name} done!')
            return redirect('run-task', taskname=task_name, trialnum=trialnum + 1)
    else:
        form = ResponseForm()
        form.instance.trialnum = trialnum
        form.instance.subject = request.user
        form.instance.parent_task = task
    context = {'taskcontext': taskcontext, 'trialnum': trialnum, 'form': form}
    return render(request, 'tasks/response_form.html', {'trial': context})


@login_required
def test_param(request, **kwargs):
    info = {'taskname': kwargs['taskname'],
            'trialnum': kwargs['trialnum']}
    return render(request, 'tasks/test.html', {'info': info})


def get_task_context(task, trialnum):
    with open(task.trialinfo.path) as fp:
        info = json.load(fp)
    stim_url = 'stimuli/' + info['stimuli'][trialnum - 1]
    prompt = info['prompt']
    instructions = info['instructions']
    choices = info['choices']
    icon_url = task.icon.url

    return {'stim_url': stim_url, 'prompt': prompt,
            'instructions': instructions, 'choices': choices,
            'icon_url': icon_url}

