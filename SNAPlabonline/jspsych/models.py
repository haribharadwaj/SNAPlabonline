from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Subject
from django.core.validators import MinLengthValidator, MinValueValidator
from .validators import taskjson_validate



# Task model for method of constant stimuli
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
        default='taskicons/task_default.png',
        help_text='Upload an image that will appear as an icon for this task')

    trialinfo = models.TextField(
        verbose_name='Trial Info',
        help_text='Paste the contents of JSON file with task information',
        validators=[taskjson_validate])

    tasktype = models.SmallIntegerField(choices=TASK_TYPES, null=True)

    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)
    task_url = models.SlugField(max_length=32, unique=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Task: {self.displayname}'


# Model for a study session that we can direct participants to
# Studies can have up to 8 different tasks
class Study(models.Model):
    title = models.CharField(default='SNAPlab Study',
        max_length=24,
        help_text='Short title for study')
    welcome_message = models.TextField(default='',
        help_text='A welcome screen message suitable for display in the landing page for your subjects')
    task1 = models.ForeignKey(Jstask, on_delete=models.SET_NULL,
        related_name='study_task1_set', null=True)
    task2 = models.ForeignKey(Jstask, on_delete=models.SET_NULL,
        related_name='study_task2_set', null=True)
    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)
    study_url = models.SlugField(max_length=32, unique=True)
    date_created = models.DateTimeField(default=timezone.now)


class OneShotResponse(models.Model):
    parent_task = models.ForeignKey(Jstask, on_delete=models.CASCADE)
    parent_study = models.ForeignKey(Study, on_delete=models.SET_NULL,
        null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    data = models.TextField()
    interactions = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'One shot response'


class SingleTrialResponse(models.Model):
    parent_task = models.ForeignKey(Jstask, on_delete=models.CASCADE)
    parent_study = models.ForeignKey(Study, on_delete=models.SET_NULL,
        null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    data = models.TextField()
    correct = models.BooleanField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    trialnum = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return 'Single Trial Response'
