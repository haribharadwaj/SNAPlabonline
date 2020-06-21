# Generated by Django 3.0.7 on 2020-06-20 20:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jspsych.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jstask',
            fields=[
                ('name', models.CharField(help_text='Short codename for task (no spaces)', max_length=24, primary_key=True, serialize=False, verbose_name='Name')),
                ('displayname', models.CharField(default='', help_text='Experimenter/Subject-friendly title or name for the task', max_length=80, verbose_name='Display Name')),
                ('descr', models.CharField(default='', help_text='Please provide a one sentence description', max_length=255, verbose_name='Short description')),
                ('icon', models.ImageField(default='taskicons/task_default.png', help_text='Upload an image that will appear as an icon for this task', upload_to='taskicons/')),
                ('trialinfo', models.TextField(help_text='Paste the contents of JSON file with task information', validators=[jspsych.validators.taskjson_validate], verbose_name='Trial Info')),
                ('tasktype', models.SmallIntegerField(choices=[(1, 'constant-fixed'), (2, 'constant-randomized')], null=True)),
                ('task_url', models.SlugField(max_length=32, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
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
                ('task1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task1_set', to='jspsych.Jstask')),
                ('task2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_task2_set', to='jspsych.Jstask')),
            ],
        ),
        migrations.CreateModel(
            name='SingleTrialResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('correct', models.BooleanField(null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('trialnum', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(2)])),
                ('parent_study', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jspsych.Study')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jspsych.Jstask')),
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
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jspsych.Jstask')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Subject')),
            ],
        ),
    ]
