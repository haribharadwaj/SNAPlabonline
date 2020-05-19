from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Task(models.Model):
    name = models.CharField(
        max_length=24,
        primary_key=True
        )

    TASK_TYPES = ((1, 'nAFC'), (2, 'Open-Set'))

    icon = models.ImageField(upload_to='taskicons/',
                             help_text='Upload an image that will appear'
                            'as an icon for this task on the home page')

    trialinfo = models.FileField(upload_to='json/')

    tasktype = models.SmallIntegerField(choices=TASK_TYPES, null=True)

    experimenter = models.ForeignKey(User, null=True,
                                     on_delete=models.SET_NULL)

    def __str__(self):
        return f'Task: {self.name}'



class Response(models.Model):
    parenttask = models.ForeignKey(Task, on_delete=models.CASCADE)
    trialnum = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])
    subject = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True)
    nafcanswer = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])
    openanswer = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'nAFC Response for task {self.parenttask.name}'

