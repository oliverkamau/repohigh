# Generated by Django 3.0 on 2022-01-05 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recievefees', '0002_feepayment_payment_receiptno'),
        ('standardcharges', '0003_auto_20211217_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeePaymentDetails',
            fields=[
                ('paymentdetail_code', models.AutoField(primary_key=True, serialize=False)),
                ('paymentdetailcharge_amount', models.DecimalField(decimal_places=2, default=0, max_digits=13)),
                ('paymentdetail_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recievefees.FeePayment')),
                ('paymentdetail_standardcharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standardcharges.StandardCharges')),
            ],
        ),
    ]
