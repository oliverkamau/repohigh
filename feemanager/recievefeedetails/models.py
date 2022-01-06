from django.db import models

from feemanager.recievefees.models import FeePayment
from setups.accounts.standardcharges.models import StandardCharges


class FeePaymentDetails(models.Model):
    paymentdetail_code = models.AutoField(primary_key=True)
    paymentdetailcharge_amount = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    paymentdetail_standardcharge = models.ForeignKey(StandardCharges, on_delete=models.CASCADE)
    paymentdetail_payment = models.ForeignKey(FeePayment, on_delete=models.CASCADE)