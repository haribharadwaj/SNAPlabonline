from django.db import models
from django.utils import timezone


# Model for anonymous subjects (not authenticated users)
class Subject(models.Model):
    subjid = models.CharField(
        max_length=32,
        primary_key=True,
        help_text='Enter your ID from Prolific (or) MTurk (or) from SNAPlab',
        verbose_name='Participant ID')
    date_added = models.DateTimeField(default=timezone.now)
    consented = models.BooleanField(default=False)

    def __str__(self):
        return f'Subject: {self.subjid}'