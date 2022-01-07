# Generated by Django 3.2.9 on 2022-01-07 09:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20211226_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 7, 15, 1, 56, 980516), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 1, 7, 9, 31, 56, 996091, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 7, 9, 31, 56, 996091, tzinfo=utc), null=True),
        ),
    ]
