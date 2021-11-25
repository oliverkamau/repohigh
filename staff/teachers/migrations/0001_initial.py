# Generated by Django 3.0 on 2021-11-23 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('responsibilities', '0001_initial'),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherSalution',
            fields=[
                ('salutation_id', models.AutoField(primary_key=True, serialize=False)),
                ('salutation_name', models.CharField(max_length=200)),
                ('salutation_desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('teacher_code', models.AutoField(primary_key=True, serialize=False)),
                ('teacher_name', models.CharField(max_length=200)),
                ('box_address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('staff_number', models.CharField(max_length=200)),
                ('date_joined', models.DateTimeField()),
                ('date_left', models.DateTimeField()),
                ('gender', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('intials', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id_no', models.CharField(max_length=200)),
                ('finger_print', models.BinaryField()),
                ('finger_print_date', models.DateTimeField()),
                ('finger_print_user', models.CharField(max_length=200)),
                ('tsc_no', models.CharField(max_length=200)),
                ('teacher_pic', models.BinaryField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.Departments')),
                ('responsibility', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='responsibilities.Responsibilities')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.TeacherSalution')),
            ],
        ),
    ]
