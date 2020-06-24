# Generated by Django 3.0.7 on 2020-06-24 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('name', models.CharField(help_text='Short codename for task (no spaces)', max_length=24, primary_key=True, serialize=False, verbose_name='Name')),
                ('displayname', models.CharField(default='', help_text='Experimenter/Subject-friendly title or name for the task', max_length=80, verbose_name='Display Name')),
                ('descr', models.CharField(default='', help_text='Please provide a one sentence description', max_length=255, verbose_name='Short description')),
                ('task_url', models.SlugField(max_length=32, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('task_type', models.PositiveSmallIntegerField(choices=[(1, 'Constant Stimulus n-AFC'), (2, 'Raw Script'), (3, 'Adaptive n-AFC'), (4, 'Open-set Speech')], default=1)),
                ('trialinfo', models.TextField(help_text='Paste the contents of JSON file or script with task information', verbose_name='Trial Info')),
                ('experimenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='SNAPlab Study', help_text='Short title for study', max_length=24)),
                ('welcome_message', models.TextField(default='', help_text='A welcome screen message suitable for display in the landing page for your subjects')),
                ('study_url', models.SlugField(max_length=32, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('experimenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('task1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task1_set', to='jspsych.Task')),
                ('task10', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task10_set', to='jspsych.Task')),
                ('task11', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task11_set', to='jspsych.Task')),
                ('task12', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task12_set', to='jspsych.Task')),
                ('task2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task2_set', to='jspsych.Task')),
                ('task3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task3_set', to='jspsych.Task')),
                ('task4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task4_set', to='jspsych.Task')),
                ('task5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task5_set', to='jspsych.Task')),
                ('task6', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task6_set', to='jspsych.Task')),
                ('task7', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task7_set', to='jspsych.Task')),
                ('task8', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task8_set', to='jspsych.Task')),
                ('task9', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task9_set', to='jspsych.Task')),
            ],
        ),
        migrations.CreateModel(
            name='SingleTrialResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('correct', models.BooleanField(null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('trialnum', models.PositiveSmallIntegerField(null=True)),
                ('parent_study', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jspsych.Study')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jspsych.Task')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='OneShotResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('interactions', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent_study', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jspsych.Study')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jspsych.Task')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Subject')),
            ],
        ),
    ]
