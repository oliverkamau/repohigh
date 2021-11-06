# Generated by Django 3.0 on 2021-11-04 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211104_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_username',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_password',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
