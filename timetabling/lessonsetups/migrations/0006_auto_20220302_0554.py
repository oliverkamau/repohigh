# Generated by Django 3.0 on 2022-03-02 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonsetups', '0005_auto_20220301_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsetups',
            name='lesson_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lessonsetups',
            name='lesson_start',
            field=models.DateTimeField(),
        ),
    ]
