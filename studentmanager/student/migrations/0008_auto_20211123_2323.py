# Generated by Django 3.0 on 2021-11-23 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20211123_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='student_statuschange_reason',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='student_statuschange_term',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]