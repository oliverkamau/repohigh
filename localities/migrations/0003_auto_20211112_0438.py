# Generated by Django 3.0 on 2021-11-12 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_studentdef_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=200)),
                ('location_code', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SubLocation',
            fields=[
                ('sublocation_id', models.AutoField(primary_key=True, serialize=False)),
                ('sublocation_name', models.CharField(max_length=200)),
                ('sublocation_code', models.CharField(max_length=200)),
                ('sublocation_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('village_id', models.AutoField(primary_key=True, serialize=False)),
                ('village_name', models.CharField(max_length=200)),
                ('village_code', models.CharField(max_length=200)),
                ('village_sublocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.SubLocation')),
            ],
        ),
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('subcounty_id', models.AutoField(primary_key=True, serialize=False)),
                ('subcounty_name', models.CharField(max_length=200)),
                ('subcounty_code', models.CharField(max_length=200)),
                ('subcounty_county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.Counties')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='location_subcounty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.SubCounty'),
        ),
    ]