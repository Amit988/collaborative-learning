# Generated by Django 3.2.8 on 2021-11-06 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answere',
            old_name='answere',
            new_name='ans',
        ),
        migrations.AddField(
            model_name='answere',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qna.answere'),
        ),
    ]
