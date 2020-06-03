# Generated by Django 3.0.6 on 2020-05-31 22:46

from django.db import migrations, models
import tasks.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200528_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_url',
            field=models.CharField(default='5LU7kFxaXzTd6P5aBEiQwNJYhGPIrp5IXDR_70f_LmA', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='trialinfo',
            field=models.FileField(help_text='JSON file with task information', upload_to='json/', validators=[tasks.validators.taskjson_validate], verbose_name='Trial Info'),
        ),
    ]