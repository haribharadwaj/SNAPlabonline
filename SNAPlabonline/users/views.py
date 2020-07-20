import csv
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.utils import timezone
from .forms import (
    UserRegisterForm,
    SubjectForm,
    ConsentForm,
    SubjectProfileForm
    )
from django.contrib.auth.decorators import (login_required,
    permission_required)
from django.core.exceptions import PermissionDenied
from .models import Subject, SubjectProfile
from .decorators import subjid_required, consent_required



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
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        next_url = request.GET.get('next')
        if form.is_valid():
            print('Posting entry form!')
            subjid = form.cleaned_data.get('subjid')
            request.session['subjid'] = subjid
            subj, was_just_created = Subject.objects.get_or_create(subjid=subjid)
            subj.latest_visit = timezone.now()
            subj.save()
            if was_just_created:
                messages.success(request,
                    f'Received your ID: {subjid}. Welcome!')
            else:
                messages.success(request,
                    f'Received your ID: {subjid}. Welcome Back!')
            return redirect(next_url)
    else:
        subjid = request.session.get('subjid', None)
        if subjid is None:
            # Check if first visit from Prolific
            subjid = request.GET.get('PROLIFIC_PID', None)
        form = SubjectForm(initial={'subjid': subjid})
    context = {'form': form, 'marketplace': 'Prolific'}
    return render(request, 'users/subject_entry_confirm.html', {'context': context})


def subject_consent(request, *args, **kwargs):
    # next_url = kwargs['next']
    if request.method == 'POST':
        form = ConsentForm(request.POST)
        next_url = request.GET.get('next')
        if form.is_valid():
            consented = form.cleaned_data.get('consented')
            subjid = request.session.get('subjid', None)
            subj = Subject.objects.get(subjid=subjid)
            subj.consented = consented
            subj.latest_consent = timezone.now()
            subj.save()
            return redirect(next_url)
    else:
        form = ConsentForm()
    context = {'form': form, 'marketplace': 'Prolific'}
    return render(request, 'users/consent.html', {'context': context})


@subjid_required
@consent_required
def core_survey(request, *args, **kwargs):
    next_url = kwargs.get('next', 'study-redirecthome')
    subjid = request.session.get('subjid', None)
    studyslug = request.session.get('studyslug', None)
    if request.method == 'POST':
        form = SubjectProfileForm(request.POST)
        if form.is_valid():
            subj = Subject.objects.get(subjid=subjid)
            form.instance.subject = subj
            form.instance.parent_study_slug = studyslug
            form.save()
            messages.success(request, f'Responses submitted for {subj.subjid}')
            return redirect(next_url)
    else:
        form = SubjectProfileForm()
    context = {'form': form, 'subjid': subjid}
    return render(request, 'users/subject_survey.html', {'context': context})


@login_required
@permission_required('jspsych.add_task', raise_exception=PermissionDenied)
def download_survey_results(request, *args, **kwargs):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="core_survey_results.csv"'

    # Any experimenter can download all profiles
    survey_fields = SubjectProfile._meta.get_fields()
    field_names = [f.name for f in survey_fields]
    profiles = SubjectProfile.objects.all()

    # Write to CSV filepointer
    writer = csv.writer(response)
    writer.writerow(field_names)
    for prof in profiles:
        vals = [getattr(prof, name) if name != 'subject' else prof.subject.subjid
                for name in field_names]
        writer.writerow(vals)

    return response


@login_required
@permission_required('jspsych.add_task', raise_exception=PermissionDenied)
def download_subjlist(request, *args, **kwargs):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="core_survey_results.csv"'

    # Any experimenter can download list of subjects
    field_names = ['subjid', 'date_added', 'consented', 'latest_visit', 'latest_consent']
    subjs = Subject.objects.all()

    # Write to CSV filepointer
    writer = csv.writer(response)
    writer.writerow(field_names)
    for subj in subjs:
        vals = [getattr(subj, name) if type(getattr(subj, name)) != datetime.datetime
                else getattr(subj, name).strftime('%d-%b-%Y %H:%M:%S (%Z)')
                for name in field_names]
        writer.writerow(vals)
    return response
