# Generated by Django 3.0 on 2022-03-01 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonsetups', '0002_lessonsetups_lesson_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonsetups',
            name='lesson_home',
        ),
    ]
