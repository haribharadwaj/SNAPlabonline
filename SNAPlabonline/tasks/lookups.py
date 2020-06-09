import json
from .models import Response, Task


def user_next_trial(task_url, user):
    # Returns: context
    # trialnum first incomplete trial for user for given task.
    # If task completed by user, returns None

    resps_user = Response.objects.filter(subject_id=user.id)
    task = Task.objects.get(task_url=task_url)
    resps_user_task = resps_user.filter(parent_task_id=task.pk)

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

    # Check if audio is external:
    serveraudio = info['serveraudio']

    done = True
    for k in range(ntrials):
        trialnum = k + 1
        if not resps_user_task.filter(trialnum=trialnum).exists():
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
            'task_name': task_name, 'serveraudio': serveraudio}
