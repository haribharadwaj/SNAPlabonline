# Generated by Django 3.0.7 on 2020-07-10 02:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subjid', models.CharField(help_text='Enter your ID from Prolific (or) MTurk (or) from SNAPlab', max_length=32, primary_key=True, serialize=False, verbose_name='Participant ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('consented', models.BooleanField(default=False)),
                ('latest_visit', models.DateTimeField(default=django.utils.timezone.now)),
                ('latest_consent', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField(help_text='Enter your age in years', null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer Not To Answer')], help_text='Please select your gender', max_length=1)),
                ('ethnicity', models.CharField(choices=[('H', 'Hispanic or Latino'), ('NH', 'NOT Hispanic or Latino'), ('N', 'Prefer Not To Answer')], help_text='Select the category that best describes you', max_length=2, null=True)),
                ('race', models.CharField(choices=[('AM', 'American Indian/Alaskan Native'), ('AS', 'Asian'), ('PI', 'Native Hawaiian or Other Pacific Islander'), ('BL', 'Black or African American'), ('WH', 'White'), ('MR', 'More than one'), ('O', 'Other'), ('N', 'Prefer Not To Answer')], help_text='Select the category that best describes you', max_length=2, null=True)),
                ('american_english', models.CharField(choices=[('Y', 'Yes'), ('NO', 'No')], help_text='For example, did you grow up in the United States/Canada from a young age (< 10 years)?', max_length=2, null=True, verbose_name='Are you a native speaker of North American English?')),
                ('neuro', models.CharField(choices=[('Y', 'Yes'), ('NO', 'No')], help_text='Choose yes only if formally diagnosed by a certified professional (e.g., medical doctor)', max_length=2, null=True, verbose_name='Have you been diagnosed with a neurological disorder?')),
                ('hl', models.CharField(choices=[('Y', 'Yes'), ('NO', 'No')], help_text='Choose yes only if formally diagnosed by a certified professional (e.g., Audiologist / ENT)', max_length=2, null=True, verbose_name='Have you been diagnosed with hearing loss?')),
                ('hl_dur', models.PositiveSmallIntegerField(blank=True, help_text='Number of years since you were first given a hearing-loss diagnosis', null=True, verbose_name='If you selected "Yes" to being diagnosed with hearing loss, how long would you say you have had hearing loss?')),
                ('hl_degree', models.CharField(blank=True, choices=[('MI', 'Mild Hearing Loss'), ('MO', 'Moderate Hearing Loss'), ('SE', 'Severe Hearing Loss'), ('SP', 'Severe-to-Profound Hearing Loss'), ('PR', 'Profound Hearing Loss'), ('UN', 'I Do Not Know'), ('O', 'Other')], help_text='If you happen to know your most recent diagnosis, please enter here', max_length=2, verbose_name='If you selected "Yes" to being diagnosed with hearing loss, what is the degree of your hearing loss')),
                ('hl_write_in', models.CharField(blank=True, help_text='In your own words, please provide any information', max_length=256, null=True, verbose_name='If you selected "Other" for degree of hearing loss, please provide further information')),
                ('hl_subjective', models.CharField(choices=[('G', 'Is similar to or better than or others my age'), ('Y', 'I have more trouble than others when there is background noise (e.g., at restaurants, busy streets)'), ('R', 'I have more trouble than others my age in most situations')], help_text='In your own assessment, how do you think your hearing compares to other people your age?', max_length=1, null=True, verbose_name='Hearing Ability')),
                ('tinnitus', models.PositiveSmallIntegerField(choices=[(0, 'Never'), (1, 'Occasionally (e.g., when it is quiet at night)'), (2, 'Persistently (it is noticeable all the time) but it does NOT bother me'), (3, 'All the time and it is bothersome, but I never sought treatment for it'), (4, 'I have bothersome tinnitus and I tried to get treatment for it')], default=0, help_text='Tinnitus is any ringing/buzzing/hissing/other sounds just in your ear when there is nothing near you that is actually producing the sound', verbose_name='Have you ever experienced tinnitus?')),
                ('music', models.PositiveSmallIntegerField(default=0, help_text='Please count up the years of instrument practice or formal vocal training you have', verbose_name='Years of music training')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Subject')),
            ],
        ),
    ]
