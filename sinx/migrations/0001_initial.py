# Generated by Django 3.2.9 on 2021-12-24 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('about', models.TextField()),
                ('link', models.URLField(max_length=2000)),
                ('overall_rating', models.IntegerField(default=0)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='sinx_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Courses-sinx',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(blank=True, max_length=3000, null=True)),
                ('rating', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sinx.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Course-Ratings',
            },
        ),
    ]