# Generated by Django 3.0 on 2022-01-21 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('floatreplenishment', '0003_floatreplenishment_float_payeebal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='floatreplenishment',
            name='float_accbal',
        ),
        migrations.RemoveField(
            model_name='floatreplenishment',
            name='float_payeebal',
        ),
        migrations.RemoveField(
            model_name='floatreplenishment',
            name='float_prevbal',
        ),
    ]