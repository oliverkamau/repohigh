# Generated by Django 3.0 on 2021-10-25 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0002_auto_20211025_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermDates',
            fields=[
                ('term_code', models.AutoField(primary_key=True, serialize=False)),
                ('term_number', models.CharField(max_length=200)),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('current_term', models.BooleanField(default=True)),
                ('term_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.SchoolClasses')),
            ],
        ),
    ]
