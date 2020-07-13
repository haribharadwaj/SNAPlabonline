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
    parent_study_slug = models.SlugField(max_length=32, null=True, blank=True)
    age = models.PositiveSmallIntegerField(help_text='Enter your age in years',
        null=True)

    
    # Useful for multiple fields
    OTHER = 'O'
    NOT_REPORTED = 'N'
    YES = 'Y'
    NO = 'NO'

    YN_choices = (
        (YES, 'Yes'),
        (NO, 'No'),
        )

    
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
        (HISPANIC, 'Hispanic or Latino'),
        (NOT_HISPANIC, 'NOT Hispanic or Latino'),
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

    ethnicity = models.CharField(max_length=2, choices=ethnicity_choices,
        help_text='Select the category that best describes you', null=True)
    race = models.CharField(max_length=2, choices=race_choices,
        help_text='Select the category that best describes you', null=True)


    american_english = models.CharField(max_length=2, choices=YN_choices, null=True,
        verbose_name='Are you a native speaker of North American English?',
        help_text='For example, did you grow up in the United States/Canada from a young age (< 10 years)?')

    
    # RIGHT = 'R'
    # LEFT = 'L'
    # BOTH = 'B'
    # handed_choices = (
    #     (RIGHT, 'Right'),
    #     (LEFT, 'Left'),
    #     (BOTH, 'I Use Both Equally')
    #     )
    # right_handed = models.CharField(max_length=1, choices=handed_choices,
    #     verbose_name='Are you right or left handed?',
    #     help_text='Select an option that best describes you')

    neuro = models.CharField(max_length=2, null=True, choices=YN_choices,
        verbose_name='Have you been diagnosed with a neurological disorder?',
        help_text=('Choose yes only if formally diagnosed by a certified professional '
            '(e.g., medical doctor)'))

    hl = models.CharField(max_length=2, null=True, choices=YN_choices,
        verbose_name='Have you been diagnosed with hearing loss?',
        help_text='Choose yes only if formally diagnosed by a certified professional (e.g., Audiologist / ENT)')

    hl_dur = models.PositiveSmallIntegerField(null=True, blank=True,
        verbose_name=('If you selected "Yes" to being diagnosed with hearing loss, '
            'for how many YEARS have you had hearing loss?'),
        help_text='Number of years since you were first given a hearing-loss diagnosis')

    MILD = 'MI'
    MODERATE = 'MO'
    SEVERE = 'SE'
    PROFOUND = 'PR'
    SEVERE_TO_PROFOUND = 'SP'
    UNKNOWN = 'UN'
    hl_degree_choices = (
        (MILD, 'Mild Hearing Loss'),
        (MODERATE, 'Moderate Hearing Loss'),
        (SEVERE, 'Severe Hearing Loss'),
        (SEVERE_TO_PROFOUND, 'Severe-to-Profound Hearing Loss'),
        (PROFOUND, 'Profound Hearing Loss'),
        (UNKNOWN, 'I Do Not Know'),
        (OTHER, 'Other')
        )

    hl_degree = models.CharField(max_length=2, blank=True,
        verbose_name=('If you selected "Yes" to being diagnosed with hearing loss, '
            'what is the degree of your hearing loss'), choices=hl_degree_choices,
        help_text='If you happen to know your most recent diagnosis, please enter here')

    hl_write_in = models.CharField(max_length=256, blank=True,
        verbose_name=('If you selected "Other" for degree of hearing loss, '
            'please provide further information'), null=True,
        help_text='In your own words, please provide any information')

    GREEN = 'G'
    YELLOW = 'Y'
    RED = 'R'
    hl_subjective_choices = (
        (GREEN, 'Is similar to (or) better than others my age'),
        (YELLOW, ('I have more trouble than others when there is background noise '
            '(e.g., at restaurants, busy streets)')),
        (RED, 'I have more trouble than others my age in most situations')
        )

    hl_subjective = models.CharField(max_length=1, null=True,
        verbose_name='Hearing Ability', choices=hl_subjective_choices,
        help_text=('In your own assessment, how do you think your hearing '
            'compares to other people your age?'))


    T0 = 0
    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4
    tinnitus_choices = (
        (T0, 'Never'),
        (T1, 'Occasionally (e.g., when it is quiet at night)'),
        (T2, 'Persistently (it is noticeable all the time) but it does NOT bother me'),
        (T3, 'All the time and it is bothersome, but I never sought treatment for it'),
        (T4, 'I have bothersome tinnitus and I tried to get treatment for it')
        )

    tinnitus = models.PositiveSmallIntegerField(choices=tinnitus_choices,
        verbose_name='Have you ever experienced tinnitus?',
        help_text='Tinnitus is any ringing/buzzing/hissing/other sounds just in your ear'
        ' when there is nothing near you that is actually producing the sound',
        default=T0)

    music = models.PositiveSmallIntegerField(verbose_name='Years of music training',
        default=0,
        help_text=('Please count up the years of '
            'instrument practice or formal vocal training you have'))

    def __str__(self):
        return f'Subject Profile: {self.subject.subjid}'