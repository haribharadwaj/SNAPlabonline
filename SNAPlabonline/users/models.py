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
    latest_visit = models.DateTimeField(default=timezone.now)
    latest_consent = models.DateTimeField(null=True)


    def __str__(self):
        return f'Subject: {self.subjid}'


# Model for storing core hearing profile and demographic info
class SubjectProfile(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True,
        help_text='Enter your age in years')

    
    # Useful for multiple fields
    OTHER = 'O'
    NOT_REPORTED = 'N'

    
    MALE = 'M'
    FEMALE = 'F'
    
    
    gender_choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_REPORTED, 'Prefer Not To Answer')
        )
    gender = models.CharField(max_length=1, choices=gender_choices,
        help_text='Please select your gender')


    HISPANIC = 'H'
    NOT_HISPANIC = 'NH'
    ethnicity_choices = (
        (HISPANIC, 'Hispanic'),
        (NOT_HISPANIC, 'NOT Hispanic'),
        (NOT_REPORTED, 'Prefer Not To Answer')
        )

    WHITE = 'WH'
    BLACK = 'BL'
    ASIAN = 'AS'
    AMERICAN_INDIAN = 'AM'
    PACIFIC_ISLANDER = 'PI'
    MULTIRACE = 'MR'


    race_choices = (
        (AMERICAN_INDIAN, 'American Indian/Alaskan Native'),
        (ASIAN, 'Asian'),
        (PACIFIC_ISLANDER, 'Native Hawaiian or Other Pacific Islander'),
        (BLACK, 'Black or African American'),
        (WHITE, 'White'),
        (MULTIRACE, 'More than one'),
        (OTHER, 'Other'),
        (NOT_REPORTED, 'Prefer Not To Answer'),
        )

    enthnicity = models.CharField(max_length=2, choices=ethnicity_choices,
        help_text='Select the category that best describes you')
    race = models.CharField(max_length=2, choices=race_choices,
        help_text='Select the category that best describes you')

    american_english = models.BooleanField(null=True,
        verbose_name='Are you a native speaker of North American English?',
        help_text='For example, did you grow up in the United States/Canada from a young age (< 10 years)?')

    RIGHT = 'R'
    LEFT = 'L'
    BOTH = 'B'
    handed_choices = (
        (RIGHT, 'Right'),
        (LEFT, 'Left'),
        (BOTH, 'I Use Both Equally')
        )
    right_handed = models.CharField(max_length=1, choices=handed_choices,
        verbose_name='Are you right or left handed?',
        help_text='Select an option that best describes you')

    neuro = models.BooleanField(null=True, verbose_name='Have you been diagnosed with a neurological disorder?',
        help_text='Choose yes only if formally diagnosed by  medical doctor')



    


