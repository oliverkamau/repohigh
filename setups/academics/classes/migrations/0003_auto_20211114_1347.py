# Generated by Django 3.0 on 2021-11-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_auto_20211025_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolclasses',
            name='admno_prefix',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
