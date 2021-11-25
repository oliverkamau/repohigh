# Generated by Django 3.0 on 2021-11-23 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Select2Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Counties',
            fields=[
                ('county_id', models.AutoField(primary_key=True, serialize=False)),
                ('county_name', models.CharField(max_length=200)),
                ('county_code', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=200)),
                ('country_continent', models.CharField(max_length=200)),
                ('country_code', models.CharField(max_length=200)),
            ],
        ),
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
        migrations.CreateModel(
            name='StudentDef',
            fields=[
                ('stdCode', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('town', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=200)),
                ('photo', models.ImageField(null=True, upload_to='parents')),
                ('stud_country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='localities.Countries')),
                ('stud_county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='localities.Counties')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='location_subcounty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.SubCounty'),
        ),
        migrations.AddField(
            model_name='counties',
            name='county_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localities.Countries'),
        ),
    ]
