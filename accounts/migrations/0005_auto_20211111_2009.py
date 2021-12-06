# Generated by Django 3.2.8 on 2021-11-11 14:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211106_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 11, 20, 9, 14, 344188), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 11, 14, 39, 14, 354303, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 11, 14, 39, 14, 354303, tzinfo=utc), null=True),
        ),
    ]