from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator

# Create your models here.
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
        help_text='Human-friendly name for the task to be used for display',
        default='',
        verbose_name= 'Display Name')
    descr = models.TextField(default='',
        help_text='Please provide a one- or two-sentence description',
        verbose_name='Short description')
    TASK_TYPES = ((1, 'nAFC'), (2, 'Open-Set'))

    icon = models.ImageField(upload_to='taskicons/',
                             help_text='Upload an image that will appear'
                            ' as an icon for this task')

    trialinfo = models.FileField(upload_to='json/',
        verbose_name='Trial Info',
        help_text='JSON file with task information')

    tasktype = models.SmallIntegerField(choices=TASK_TYPES, null=True)

    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)

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

    def __str__(self):
        return f'nAFC Response for task {self.parent_task.name}'

