# Generated by Django 3.0.7 on 2020-06-16 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='latest_visit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
