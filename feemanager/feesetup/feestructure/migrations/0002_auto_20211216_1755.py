# Generated by Django 3.0 on 2021-12-16 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feestructure', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feestructure',
            name='structure_Standardcharge',
        ),
        migrations.RemoveField(
            model_name='feestructure',
            name='structure_ammount',
        ),
    ]
