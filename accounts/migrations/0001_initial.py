# Generated by Django 3.2.9 on 2022-01-14 12:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='clubInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dateoffound', models.DateTimeField(auto_now_add=True)),
                ('logo', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[300, 300], upload_to='images/')),
                ('vision_and_mission', models.TextField(blank=True, null=True)),
                ('tag', models.CharField(default='ALL', max_length=1000)),
                ('tagline', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Club-Info',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='DigiWeek', max_length=500)),
                ('content', models.TextField()),
                ('poster', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[300, 300], upload_to='posters/')),
                ('event_date', models.DateField(blank=True, null=True)),
                ('event_time', models.TimeField(blank=True, default=datetime.datetime(2022, 1, 14, 18, 23, 33, 371986), null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clubevents', to='accounts.clubinfo')),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=3000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(default='Empty')),
                ('views', models.IntegerField()),
                ('private', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
                ('tag', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stories',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('msg', models.TextField()),
                ('club', models.ForeignKey(default='cosb', on_delete=django.db.models.deletion.CASCADE, related_name='clubstask', to='accounts.clubinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Club-Discussions',
            },
        ),
        migrations.CreateModel(
            name='WaitingArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Waiting-Area',
            },
        ),
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Visitors',
            },
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskviews', to='accounts.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('task', models.ManyToManyField(related_name='done', to='accounts.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Task-status',
            },
        ),
        migrations.CreateModel(
            name='TaskRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.task')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Club-Discussions-Updates',
            },
        ),
        migrations.CreateModel(
            name='StoryAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(blank=True, upload_to='audio/')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.story')),
            ],
        ),
        migrations.CreateModel(
            name='ReportClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ManyToManyField(blank=True, related_name='clubs', to='accounts.clubInfo')),
                ('memname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberofclubs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Member's",
            },
        ),
        migrations.CreateModel(
            name='jSecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField(blank=True, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jsecsclub', to='accounts.clubinfo')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Jsec's",
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=255)),
                ('course', models.CharField(max_length=255)),
                ('branch', models.CharField(max_length=255)),
                ('sem', models.CharField(max_length=20)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('is_verified', models.CharField(default='NO', max_length=3)),
                ('auth_token', models.CharField(default='nothing', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Extrainfo-about-user',
            },
        ),
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Feedbacks',
            },
        ),
        migrations.CreateModel(
            name='EventUpdates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Event-Updates',
            },
        ),
        migrations.CreateModel(
            name='eventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='accounts.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userevents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Event-Registrations',
            },
        ),
        migrations.CreateModel(
            name='eventRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='eventComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Event-Comments',
            },
        ),
        migrations.CreateModel(
            name='ContentCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('msg', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Clubverification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('clg', models.CharField(default='Not Required', max_length=1000)),
                ('is_verified', models.BooleanField(default=False)),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
            ],
            options={
                'verbose_name_plural': 'Verified Clubs',
            },
        ),
        migrations.CreateModel(
            name='ClubRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=10)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.clubinfo')),
            ],
        ),
    ]
