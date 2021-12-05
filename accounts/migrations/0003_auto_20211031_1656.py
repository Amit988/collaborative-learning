# Generated by Django 3.2.8 on 2021-10-31 11:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211031_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 10, 31, 16, 55, 59, 633854), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 31, 11, 25, 59, 633854, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 10, 31, 11, 25, 59, 633854, tzinfo=utc), null=True),
        ),
    ]
