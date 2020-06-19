# Generated by Django 3.0.7 on 2020-06-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200618_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectprofile',
            name='enthnicity',
        ),
        migrations.RemoveField(
            model_name='subjectprofile',
            name='hl_type',
        ),
        migrations.AddField(
            model_name='subjectprofile',
            name='ethnicity',
            field=models.CharField(choices=[('H', 'Hispanic or Latino'), ('NH', 'NOT Hispanic or Latino'), ('N', 'Prefer Not To Answer')], help_text='Select the category that best describes you', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='subjectprofile',
            name='hl_degree',
            field=models.CharField(choices=[('MI', 'Mild Hearing Loss'), ('MO', 'Moderate Hearing Loss'), ('SE', 'Severe Hearing Loss'), ('SP', 'Severe-to-Profound Hearing Loss'), ('PR', 'Profound Hearing Loss'), ('UN', 'I Do Not Know'), ('O', 'Other')], default='UN', help_text='If you happen to know you what degree you were diagnosed with, please enter here', max_length=2, verbose_name='Degree of hearing loss'),
        ),
        migrations.AlterField(
            model_name='subjectprofile',
            name='race',
            field=models.CharField(choices=[('AM', 'American Indian/Alaskan Native'), ('AS', 'Asian'), ('PI', 'Native Hawaiian or Other Pacific Islander'), ('BL', 'Black or African American'), ('WH', 'White'), ('MR', 'More than one'), ('O', 'Other'), ('N', 'Prefer Not To Answer')], help_text='Select the category that best describes you', max_length=2, null=True),
        ),
    ]