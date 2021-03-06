import json
from secrets import token_urlsafe
from .models import (
    SingleTrialResponse,
    Task,
    OneShotResponse,
    )
from users.models import Subject


# Creates a cryptopgraphically good slug unique for task
def create_task_slug(length=24):
    # Note length here us bytes of randomness
    # URLsafe is base64, so you get 24*1.3 = 32 chars
    while True:
        # Generate url-safe token
        link = token_urlsafe(length)
        # Check if token is already used by a Task instance
        if not Task.objects.filter(task_url=link):
            # If token not in use, then done
            break
    return link


# Creates a cryptopgraphically good slug unique for study
def create_study_slug(length=24):
    # Note length here us bytes of randomness
    # URLsafe is base64, so you get 24*1.3 = 32 chars
    while True:
        # Generate url-safe token
        link = token_urlsafe(length)
        # Check if token is already used by a Task instance
        if not Study.objects.get(task_url=link):
            # If token not in use, then done
            break
    return link


def subj_next_trial(task_url, subject):
    # Returns: context
    # trialnum first incomplete trial for subject for given task.
    # If task completed by subject, returns None

    resps_subject = SingleTrialResponse.objects.filter(subject_id=subject)
    task = Task.objects.get(task_url=task_url)
    resps_subject_task = resps_subject.filter(parent_task_id=task.pk)

    display_name = task.displayname
    task_name = task.name

    
    info = json.loads(task.trialinfo)

    # Overall info
    instructions = info['instructions']
    feedback = info['feedback']

    # Get trials info from task
    trials = info['trials']
    ntrials = len(trials)

    # Get icon from task
    icon_url = task.icon.url

    # Check if audio is external
    serveraudio = info['serveraudio']

    done = True
    for k in range(ntrials):
        trialnum = k + 1
        if not resps_subject_task:
            done = False
            break
    if done:
        trialnum = None

    # If there are more trials to be done:
    if trialnum is not None:
        k = trialnum - 1  # Python index starts at zero
        if serveraudio:
            stim_url = 'stimuli/' + trials[k]['stimulus']
        else:
            stim_url = trials[k]['stimulus']

        prompt = trials[k]['prompt']
        choices = trials[k]['choices']
        answer = trials[k]['answer']
        progress = k * 100./ntrials
    else:
        stim_url = None
        prompt = ''
        choices = []
        answer = None
        progress = 100.

    return {'stim_url': stim_url, 'prompt': prompt,
            'instructions': instructions, 'choices': choices,
            'icon_url': icon_url, 'done': done,
            'ntrials': ntrials, 'progress': progress,
            'feedback': feedback, 'answer': answer,
            'trialnum': trialnum, 'display_name': display_name,
            'task_name': task_name, 'serveraudio': serveraudio,
            'subject': subject}


def get_task_context(task_url, subject, studyslug):
    task = Task.objects.get(task_url=task_url)
    display_name = task.displayname
    task_name = task.name

    info = json.loads(task.trialinfo)

    # Overall info
    instructions = info['instructions']
    feedback = info['feedback']
    isi = info['isi']
    holdfeedback = info['holdfeedback']
    randomize = info['randomize']

    # Get trials info from task
    trials = info['trials']
    voltrials = info['volume']

    # Check if audio is external
    serveraudio = info['serveraudio']

    resps_subject = OneShotResponse.objects.filter(subject_id=subject)
    resps_subject_task = resps_subject.filter(parent_task_id=task.pk)

    if resps_subject_task.filter(parent_study_slug=studyslug).exists():
        done = True
    else:
        done = False

    return {'instructions': instructions, 'trials': trials,
            'feedback': feedback, 'display_name': display_name,
            'task_name': task_name, 'serveraudio': serveraudio,
            'subject': subject, 'done': done, 'voltrials': voltrials,
            'task_url': task_url, 'isi': isi,
            'holdfeedback': holdfeedback, 'randomize': randomize}


def get_task_results(task_url, experimenter):
    task = Task.objects.get(task_url=task_url)
    if task.experimenter != experimenter:
        return (None, None)
    else:
        resps = OneShotResponse.objects.filter(parent_task=task)
        info = []
        for resp in resps:
            resp_info = json.loads(resp.data)
            info += [resp_info]
        fname = task.name + '_' + experimenter.username + '_results.json'
        return (info, fname)



def get_scores(taskslug, studyslug, subjid):
    task = Task.objects.get(task_url=taskslug)
    resp_all = OneShotResponse.objects.filter(parent_task=task)
    resp_study = resp_all.filter(parent_study_slug=studyslug)
    scores = []  # One entry per conditions
    if resp_study.filter(subject_id=subjid).exists():
        # Normally only one entry per study per subject per task is expected
        resp = resp_study.filter(subject_id=subjid).latest('date_posted')
        dat = json.loads(resp.data)
        # At most, you can have as many conditions as trial entries
        # Usually lot fewer
        Nmax = len(dat)
        nconds = 0
        for c in range(Nmax):
            for trial in dat:
                if 'cond' in trial.keys():
                    if trial['cond'] == (c + 1):
                        nconds += 1
                        break

        for c in range(nconds):
            ncorrect = 0.
            ntotal = 0.
            for trial in dat:
                if 'cond' in trial.keys():
                    if trial['cond'] == (c + 1):
                        ntotal += 1
                        if trial['correct'] == True:
                            ncorrect += 1.
            if ntotal == 0:
                # Extra check to avoid ZeroDivision
                score = 0
            else:
                score = ncorrect * 100. / ntotal
            scores += [score,]
    # If scores is empty =>
    # then subject didn't complete task within this study
    return scores



