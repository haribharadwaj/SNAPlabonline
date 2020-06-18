from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import (
    UserRegisterForm,
    SubjectForm,
    ConsentForm
    )
from .models import Subject

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def subject_entry(request, *args, **kwargs):
    next_url = kwargs['next']
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            print('Posting entry form!')
            subjid = form.cleaned_data.get('subjid')
            request.session['subjid'] = subjid
            subj, was_just_created = Subject.objects.get_or_create(subjid=subjid)
            subj.latest_visit = timezone.now()
            subj.save()
            if was_just_created:
                messages.success(request,
                    f'Successfully enrolled {subjid} in the study. Welcome!')
            else:
                messages.success(request,
                    f'Successfully enrolled {subjid} in the study. Welcome Back!')
            return redirect(next_url)
    else:
        subjid = request.session.get('subjid', None)
        form = SubjectForm(initial={'subjid': subjid})
    context = {'form': form, 'marketplace': 'Prolific'}
    return render(request, 'users/subject_entry_confirm.html', {'context': context})


def subject_consent(request, *args, **kwargs):
    next_url = kwargs['next']
    if request.method == 'POST':
        form = ConsentForm(request.POST)
        if form.is_valid():
            consented = form.cleaned_data.get('consented')
            subjid = request.session.get('subjid', None)
            subj = Subject.objects.get(subjid=subjid)
            subj.consented = consented
            subj.latest_consent = timezone.now()
            subj.save()

            messages.success(request,
                    f'Your consent to has been recorded. Thank you!')
            return redirect(next_url)
    else:
        form = ConsentForm()
    context = {'form': form, 'marketplace': 'Prolific'}
    return render(request, 'users/consent.html', {'context': context})