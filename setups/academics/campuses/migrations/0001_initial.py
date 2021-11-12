# Generated by Django 3.0 on 2021-11-12 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('localities', '0003_auto_20211112_0438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campuses',
            fields=[
                ('campus_code', models.AutoField(primary_key=True, serialize=False)),
                ('campus_name', models.CharField(max_length=200)),
                ('campus_incharge', models.CharField(max_length=200)),
                ('campus_inchargephone', models.CharField(max_length=200)),
                ('campus_location', models.CharField(max_length=200)),
                ('campus_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='localities.Counties')),
            ],
        ),
    ]
