# Generated by Django 3.0 on 2022-01-21 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accountmaster', '0002_accountmaster_account_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='PettyCashPayments',
            fields=[
                ('pettycash_code', models.AutoField(primary_key=True, serialize=False)),
                ('pettycash_payee', models.CharField(max_length=200)),
                ('pettycashdoc_no', models.CharField(blank=True, max_length=200, null=True)),
                ('pettycash_amount', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('pettycash_amountwording', models.CharField(blank=True, max_length=200, null=True)),
                ('pettycash_date', models.DateTimeField()),
                ('pettycash_transdescription', models.CharField(max_length=500)),
                ('pettycash_voucherno', models.CharField(blank=True, max_length=200, null=True)),
                ('pettycash_receiptno', models.CharField(blank=True, max_length=200, null=True)),
                ('pettycash_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountmaster.AccountMaster')),
                ('pettycash_paidby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
