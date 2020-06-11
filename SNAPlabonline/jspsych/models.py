from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from secrets import token_urlsafe
from .validators import taskjson_validate


# Create your models here.

class Jstask(models.Model):
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

    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)
    task_url = models.CharField(max_length=32, unique=True,
        default=token_urlsafe(32))
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Task: {self.displayname}'


class OneShotResponse(models.Model):
    parent_task = models.ForeignKey(Jstask, on_delete=models.CASCADE)
    data = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'One shot response'


class SingleTrialResponse(models.Model):
    parent_task = models.ForeignKey(Jstask, on_delete=models.CASCADE)
    data = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Single Trial Response'