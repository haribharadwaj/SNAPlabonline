from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator
from .validators import taskjson_validate
from secrets import token_urlsafe



# Creates a cryptopgraphically good slug unique for task
def create_task_slug(length=32):
    while True:
        # Generate url-safe token
        link = token_urlsafe(length)
        # Check if token is already used by a Jstask instance
        if not Task.objects.filter(task_url=link):
            # If token not in use, then done
            break
    return link


'''
Model that holds task information.
A separate model for trials is not created:
This is because, response options for each trial
should ideally be a list of variable length,
and the best way to do that within is a db is 
using strings/text anyway. So decide to keep
such info within json file and lookup at runtime.
'''

class Task(models.Model):
    name = models.CharField(
        max_length=24,
        primary_key=True,
        help_text='Short codename for task (no spaces)',
        verbose_name='Name')
    displayname = models.CharField(max_length=80,
        help_text='Experimenter/Subject-friendly title or name for the task',
        default='',
        verbose_name= 'Display Name')
    descr = models.CharField(max_length=255, default='',
        help_text='Please provide a one sentence description',
        verbose_name='Short description')
    TASK_TYPES = (
        (1, 'constant-fixed'),
        (2, 'constant-randomized')
        )

    icon = models.ImageField(upload_to='taskicons/',
                             help_text='Upload an image that will appear'
                            ' as an icon for this task')

    trialinfo = models.TextField(
        verbose_name='Trial Info',
        help_text='Paste the contents of JSON file with task information',
        validators=[taskjson_validate])

    tasktype = models.SmallIntegerField(choices=TASK_TYPES, null=True)

    # Setting related_name because there is Task model in jspsych
    # with foreignkey to User
    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='serverside_task_set')
    task_url = models.CharField(max_length=32, unique=True,
        default=create_task_slug)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Task: {self.displayname}'



class Response(models.Model):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    trialnum = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])
    subject = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True)
    answer = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])
    date_posted = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(null=True)

    def __str__(self):
        return f'nAFC Response for task {self.parent_task.name}'


