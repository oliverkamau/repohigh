from django.db import models

class StandardCharges(models.Model):
    charge_code = models.AutoField(primary_key=True)
    charge_name = models.CharField(max_length=200)
    charge_uiid = models.CharField(max_length=200)
    charge_priority = models.IntegerField(default=0)
    charge_acc_code = models.CharField(max_length=200, blank=True, null=True)
    charge_refundable = models.BooleanField(default=False)
    charge_type = models.CharField(max_length=200, blank=True, null=True)
    charge_acc = models.CharField(max_length=200, blank=True, null=True)
    charge_active = models.BooleanField(default=True)