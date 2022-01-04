# Generated by Django 3.0 on 2022-01-03 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentModes',
            fields=[
                ('payment_code', models.AutoField(primary_key=True, serialize=False)),
                ('payment_name', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_desc', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_minamount', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('payment_maxamount', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
            ],
        ),
    ]
