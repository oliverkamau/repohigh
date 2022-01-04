from django.db import models

# Create your models here.

class PaymentModes(models.Model):
    payment_code = models.AutoField(primary_key=True)
    payment_name = models.CharField(max_length=200, null=True, blank=True)
    payment_desc = models.CharField(max_length=200, null=True, blank=True)
    payment_minamount = models.DecimalField(max_digits=13,decimal_places=2,default=0)
    payment_maxamount = models.DecimalField(max_digits=13,decimal_places=2,default=0)
