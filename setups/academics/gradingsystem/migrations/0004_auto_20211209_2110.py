# Generated by Django 3.0 on 2021-12-09 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gradingschemes', '0001_initial'),
        ('gradingsystem', '0003_gradingsystem_grading_scheme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradingsystem',
            name='grading_scheme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gradingschemes.GradingSchemes'),
        ),
    ]
