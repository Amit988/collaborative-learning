# Generated by Django 3.2.9 on 2022-01-07 12:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20220107_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 7, 18, 25, 52, 265680), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 1, 7, 12, 55, 52, 281312, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 7, 12, 55, 52, 281312, tzinfo=utc), null=True),
        ),
    ]