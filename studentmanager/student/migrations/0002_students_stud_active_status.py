# Generated by Django 3.0 on 2021-11-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='stud_active_status',
            field=models.BooleanField(default=True),
        ),
    ]
