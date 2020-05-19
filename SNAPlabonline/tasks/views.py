import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskCreationForm, RunTrialForm

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
def run_task(request, trialnum=1):
    if request.method == 'POST':
        form = RunTrialForm(request.POST)
        form.instance.subject = request.user
        form.instance.trialnum = trialnum
        if form.is_valid():
            form.save()
            taskname = form.cleaned_data.get('name')
            messages.success(request, f'{taskname} task created!')
            return redirect('tasks-home')
    else:
        form = RunTrialForm()
    return render(request, 'tasks/run_task.html', {'form': form})