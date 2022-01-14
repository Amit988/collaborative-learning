# Generated by Django 3.2.9 on 2022-01-13 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qna', '0002_clubquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubQuestionAnswere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qna.clubquestionanswere')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qna.clubquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Answeres',
            },
        ),
    ]
