# Generated by Django 3.2.9 on 2022-01-08 07:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220107_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 8, 13, 15, 59, 677226), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 1, 8, 7, 45, 59, 677226, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 8, 7, 45, 59, 677226, tzinfo=utc), null=True),
        ),
    ]
