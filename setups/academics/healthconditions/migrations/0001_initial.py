# Generated by Django 3.0 on 2021-11-12 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthStatus',
            fields=[
                ('healthcondition_code', models.AutoField(primary_key=True, serialize=False)),
                ('healthcondition_name', models.CharField(max_length=200)),
                ('healthcondition_desc', models.CharField(max_length=400)),
            ],
        ),
    ]
