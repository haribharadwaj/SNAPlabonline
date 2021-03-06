from django.db import models
from jspsych.models import Task
from django.contrib.auth.models import User
from users.models import Subject
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Use multitable inheritance (essentially OneToOneField mapping)
class BaseNode(models.Model):
    parent_node = models.ForeignKey('self', null=True,
        related_name='parentof_set',
        on_delete=models.CASCADE)  # Delete subtree if parent gone
    child_node = models.ForeignKey('self', null=True,
        related_name='childof_set',
        on_delete=models.SET_NULL) # Keep parent if child deleted
    ROOT = 'Root'
    TASK = 'Task'
    FORK = 'Fork'
    node_types = (
        (ROOT, 'Start of the study'),
        (TASK, 'Task'),
        (FORK, 'Decision Rule')
        )
    node_type = models.CharField(max_length=4,
        choices=node_types)
    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)


class StudyRoot(BaseNode):
    name = models.CharField(
        max_length=24,
        primary_key=True,
        help_text='Short codename for study (no spaces)',
        verbose_name='Name')
    slug = models.SlugField(max_length=32, unique=True)
    displayname = models.CharField(max_length=80,
        help_text='Experimenter/Subject-friendly title or name for the study',
        default='SNAPlab Hearing Study',
        verbose_name= 'Display Name')
    addcoresurvey = models.BooleanField(default=False, blank=True,
        verbose_name='Add core survey to study?',
        help_text='Check the box to add our core survey as the first item in the study')
    descr = models.CharField(max_length=255, default='',
        help_text='Please provide a one sentence description',
        verbose_name='Short description')
    end_url = models.URLField(verbose_name='End URL', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Study: {self.displayname}'


class TaskNode(BaseNode):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    pay = models.DecimalField(max_digits=4, decimal_places=2,
        default=0.00, null=True,
        verbose_name='Compensation (US$)')


class BranchNode(BaseNode):
    child_alternate = models.ForeignKey(BaseNode, null=True,
        related_name='altnodeof_set',
        on_delete=models.SET_NULL)
    SCORE_GREATER = 'ScGr'
    SCORE_LESSER = 'ScLs'
    check_choices = (
        (SCORE_GREATER, 'Scored Greater Than'),
        (SCORE_LESSER, 'Scored Less Than')
        )
    threshold = models.SmallIntegerField(default=-1,
        validators=[MinValueValidator(-1), MaxValueValidator(100)])
    condition = models.PositiveSmallIntegerField(default=1)
    check_type = models.CharField(max_length=4,
        choices=check_choices, default=SCORE_GREATER)
