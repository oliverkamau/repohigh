# Generated by Django 3.0 on 2021-12-09 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradingsystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradingsystem',
            name='default_system',
            field=models.BooleanField(default=False),
        ),
    ]
