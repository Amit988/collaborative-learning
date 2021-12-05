# Generated by Django 3.2.8 on 2021-11-06 05:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 6, 11, 0, 38, 457401), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 6, 5, 30, 38, 526799, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 6, 5, 30, 38, 526799, tzinfo=utc), null=True),
        ),
    ]
