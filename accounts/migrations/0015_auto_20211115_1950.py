# Generated by Django 3.2.8 on 2021-11-15 14:20

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0014_auto_20211115_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 15, 19, 50, 56, 389629), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 15, 14, 20, 56, 389629, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 11, 15, 14, 20, 56, 389629, tzinfo=utc), null=True),
        ),
        migrations.RemoveField(
            model_name='waitingarea',
            name='user',
        ),
        migrations.AddField(
            model_name='waitingarea',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
