# Generated by Django 3.0.7 on 2020-06-17 05:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200616_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='latest_visit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]