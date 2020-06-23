from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Subject
from django.core.validators import MinLengthValidator, MinValueValidator
from .validators import taskjson_validate



# Base task model for storing most fields shared by all task types
# The idea is to multi-table inheritance, so this will create dbtable
# However, objects of should NOT be created in order for child lookup
# This makes possible one response and study model regardless of task type
class BaseTask(models.Model):
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
    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)
    task_url = models.SlugField(max_length=32, unique=True)
    date_created = models.DateTimeField(default=timezone.now)

    # Store task type in base task
    CONST_STIM = 1
    RAW = 2
    ADAPTIVE = 3
    OPEN_SPEECH = 4
    choices_type = (
        (CONST_STIM, 'Constant Stimulus n-AFC'),
        (RAW, 'Raw Script'),
        (ADAPTIVE, 'Adaptive n-AFC'),
        (OPEN_SPEECH, 'Open-set Speech')
        )
    task_type = models.PositiveSmallIntegerField(choices=choices_type,
        default=CONST_STIM)

    def __str__(self):
        return f'Task: {self.displayname}'


# Task model for method of constant stimuli
class ConstStimTask(BaseTask):
    trialinfo = models.TextField(
        verbose_name='Trial Info',
        help_text='Paste the contents of JSON file with task information',
        validators=[taskjson_validate])


# Task model for arbitrary jspsych script
class RawTask(BaseTask):
    taskscript = models.TextField(
        verbose_name='Task Script',
        help_text='Paste the jsPsych code here, just the javascript part')


class AdaptiveTask(BaseTask):
    tasksinfo = models.TextField(
        verbose_name='Task Details',
        help_text='Paste the contents of JSON file for adaptive n-AFC task')


class OpenSpeechTask(BaseTask):
    tasksinfo = models.TextField(
        verbose_name='Task Details',
        help_text='Paste the contents of JSON file for adaptive 3-AFC task')


# Model for a study session that we can direct participants to
# Studies can have up to 12 different tasks
class Study(models.Model):
    title = models.CharField(default='SNAPlab Study',
        max_length=24,
        help_text='Short title for study')
    welcome_message = models.TextField(default='',
        help_text=('A welcome screen message suitable for display '
            'in the landing page for your subjects'))
    task1 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task1_set', null=True)
    task2 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task2_set', null=True)
    task3 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task3_set', null=True)
    task4 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task4_set', null=True)
    task5 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task5_set', null=True)
    task6 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task6_set', null=True)
    task7 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task7_set', null=True)
    task8 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task8_set', null=True)
    task9 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task9_set', null=True)
    task10 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task10_set', null=True)
    task11 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task11_set', null=True)
    task12 = models.ForeignKey(BaseTask, on_delete=models.SET_NULL,
        related_name='study_task12_set', null=True)

    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)
    study_url = models.SlugField(max_length=32, unique=True)
    date_created = models.DateTimeField(default=timezone.now)


class OneShotResponse(models.Model):
    parent_task = models.ForeignKey(BaseTask, on_delete=models.CASCADE)
    parent_study = models.ForeignKey(Study, on_delete=models.SET_NULL,
        null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    data = models.TextField()
    interactions = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'One shot response'


class SingleTrialResponse(models.Model):
    parent_task = models.ForeignKey(BaseTask, on_delete=models.CASCADE)
    parent_study = models.ForeignKey(Study, on_delete=models.SET_NULL,
        null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    data = models.TextField()
    correct = models.BooleanField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    trialnum = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return 'Single Trial Response'
