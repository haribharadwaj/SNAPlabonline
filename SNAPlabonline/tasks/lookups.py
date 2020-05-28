import json
from .models import Response

def get_task_context(task, trialnum, user):
    icon_url = task.icon.url
    with open(task.trialinfo.path) as fp:
        info = json.load(fp)

    # Overall info
    instructions = info['instructions']
    feedback = info['feedback']

    # Trial level info
    trials = info['trials']
    ntrials = len(trials)
    k = trialnum - 1  # Python index starts at zero

    if trialnum <= ntrials:
        stim_url = 'stimuli/' + trials[k]['stimulus']
        prompt = trials[k]['prompt']
        choices = trials[k]['choices']
        no_more_trials = False
        answer = trials[k]['answer']
    else:
        stim_url = None
        no_more_trials = True
        prompt = ''
        choices = []
        answer = None

    done = user_completed_task(task.pk, user, ntrials)
    progress = (trialnum - 1) * 100./ntrials

    return {'stim_url': stim_url, 'prompt': prompt,
            'instructions': instructions, 'choices': choices,
            'icon_url': icon_url, 'done': done,
            'no_more_trials': no_more_trials,
            'ntrials': ntrials, 'progress': progress,
            'feedback': feedback, 'answer': answer}

def user_completed_task(task_id, user, ntrials):
    resps_user = Response.objects.filter(subject_id=user.id)
    resps_user_task = resps_user.filter(parent_task_id=task_id)

    for k in range(ntrials):
        if not resps_user_task.filter(trialnum=(k+1)).exists():
            return False
    # If response to all trials exist, then:
    return True