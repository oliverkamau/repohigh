# Generated by Django 3.0 on 2022-01-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemParameters',
            fields=[
                ('parameter_code', models.AutoField(primary_key=True, serialize=False)),
                ('parameter_name', models.CharField(max_length=200)),
                ('parameter_desc', models.CharField(max_length=400)),
                ('parameter_status', models.BooleanField(default=True)),
                ('parameter_value', models.CharField(max_length=200)),
            ],
        ),
    ]