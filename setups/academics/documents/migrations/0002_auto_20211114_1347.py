# Generated by Django 3.0 on 2021-11-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document_desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]