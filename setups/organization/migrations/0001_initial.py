# Generated by Django 3.0 on 2022-01-31 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organization_code', models.AutoField(primary_key=True, serialize=False)),
                ('organization_name', models.CharField(blank=True, max_length=200, null=True)),
                ('physical_address', models.CharField(blank=True, max_length=400, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=400, null=True)),
                ('organization_telno', models.CharField(blank=True, max_length=200, null=True)),
                ('organization_cellno', models.CharField(blank=True, max_length=200, null=True)),
                ('organization_mission', models.CharField(blank=True, max_length=400, null=True)),
                ('organization_vision', models.CharField(blank=True, max_length=400, null=True)),
                ('organization_motto', models.CharField(blank=True, max_length=400, null=True)),
                ('organization_websites', models.CharField(blank=True, max_length=200, null=True)),
                ('organization_email', models.CharField(blank=True, max_length=200, null=True)),
                ('adm_date', models.DateTimeField(blank=True, null=True)),
                ('organization_logo', models.ImageField(blank=True, null=True, upload_to='orglogos')),
            ],
        ),
    ]
