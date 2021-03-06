# Generated by Django 3.0.7 on 2020-07-10 02:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jspsych', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_type', models.CharField(choices=[('Root', 'Start of the study'), ('Task', 'Task'), ('Fork', 'Decision Rule')], max_length=4)),
                ('child_node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childof_set', to='studytree.BaseNode')),
                ('experimenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent_node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentof_set', to='studytree.BaseNode')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRoot',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='studytree.BaseNode')),
                ('name', models.CharField(help_text='Short codename for study (no spaces)', max_length=24, primary_key=True, serialize=False, verbose_name='Name')),
                ('slug', models.SlugField(max_length=32, unique=True)),
                ('displayname', models.CharField(default='SNAPlab Hearing Study', help_text='Experimenter/Subject-friendly title or name for the study', max_length=80, verbose_name='Display Name')),
                ('descr', models.CharField(default='', help_text='Please provide a one sentence description', max_length=255, verbose_name='Short description')),
                ('end_url', models.URLField(blank=True, null=True, verbose_name='End URL')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            bases=('studytree.basenode',),
        ),
        migrations.CreateModel(
            name='TaskNode',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='studytree.BaseNode')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jspsych.Task')),
            ],
            bases=('studytree.basenode',),
        ),
        migrations.CreateModel(
            name='BranchNode',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='studytree.BaseNode')),
                ('threshold', models.SmallIntegerField(default=-1, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(100)])),
                ('condition', models.PositiveSmallIntegerField(default=1)),
                ('check_type', models.CharField(choices=[('ScGr', 'Scored Greater Than'), ('ScLs', 'Scored Less Than')], default='ScGr', max_length=4)),
                ('child_alternate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='altnodeof_set', to='studytree.BaseNode')),
            ],
            bases=('studytree.basenode',),
        ),
    ]
