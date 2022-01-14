# Generated by Django 3.2.9 on 2022-01-11 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20220111_2048'),
        ('course_diary', '0002_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(default="Hey, Look at this course it's quite popular on cosb diary.")),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_diary.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
