# Generated by Django 3.0 on 2021-11-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20211123_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='student_resume_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]