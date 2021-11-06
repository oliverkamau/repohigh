# Generated by Django 3.0 on 2021-10-30 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proffessions', '0001_initial'),
        ('parents', '0002_parents_parent_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='excel')),
            ],
        ),
        migrations.AlterField(
            model_name='parents',
            name='father_proffession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='father_proffession_foreignkey', to='proffessions.Proffessions'),
        ),
        migrations.AlterField(
            model_name='parents',
            name='mother_proffession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother_proffession_foreignkey', to='proffessions.Proffessions'),
        ),
    ]