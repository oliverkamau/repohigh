# Generated by Django 3.0 on 2022-03-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonsetups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonsetups',
            name='lesson_home',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
