# Generated by Django 3.0 on 2021-11-12 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentStatus',
            fields=[
                ('status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=200)),
                ('status_desc', models.CharField(max_length=200)),
            ],
        ),
    ]