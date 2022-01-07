# Generated by Django 3.2.9 on 2022-01-07 12:55

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
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=5000)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, size=[300, 300], upload_to='images/')),
                ('about', models.TextField(blank=True, null=True)),
                ('link', models.URLField(max_length=2000)),
                ('overall_rating', models.IntegerField(default=0)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='course_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Courses-sinx',
                'ordering': ['-overall_rating'],
            },
        ),
        migrations.CreateModel(
            name='TotalRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_rating', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sinx.course')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(blank=True, max_length=3000, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sinx.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Course-Ratings',
            },
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catagory', models.CharField(default='Computer Science', max_length=250)),
                ('platform', models.CharField(default='YouTube', max_length=1000)),
                ('released_date', models.DateField(blank=True, null=True)),
                ('country', models.CharField(default='India', max_length=1000)),
                ('language', models.CharField(default='English', max_length=250)),
                ('price', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=4)),
                ('certificate', models.BooleanField(default=False)),
                ('material_type', models.CharField(choices=[('Videos', 'Videos'), ('Textual', 'Textual'), ('Hybrid', 'Hybrid')], default='Videos', max_length=25)),
                ('added_by', models.CharField(default='Neesham', max_length=1000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_details', to='sinx.course')),
            ],
            options={
                'verbose_name_plural': 'Courses-details',
            },
        ),
    ]