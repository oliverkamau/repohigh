# Generated by Django 3.0 on 2021-10-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proffessions',
            fields=[
                ('proffesion_id', models.AutoField(primary_key=True, serialize=False)),
                ('proffesion_name', models.CharField(max_length=200)),
                ('proffesion_desc', models.CharField(max_length=200)),
            ],
        ),
    ]