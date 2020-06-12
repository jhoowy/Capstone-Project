# Generated by Django 3.0.6 on 2020-06-03 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='processed',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='videos',
            name='progress_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videos',
            name='total_frame',
            field=models.IntegerField(default=0),
        ),
    ]