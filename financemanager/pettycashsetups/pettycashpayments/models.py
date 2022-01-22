from django.db import models

# Create your models here.
from setups.accounts.accountmaster.models import AccountMaster
from useradmin.users.models import User


class PettyCashPayments(models.Model):
    pettycash_code = models.AutoField(primary_key=True)
    pettycash_payee = models.CharField(max_length=200)
    pettycashdoc_no = models.CharField(max_length=200, null=True, blank=True)
    pettycash_amount = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    pettycash_amountwording = models.CharField(max_length=200, null=True, blank=True)
    pettycash_date = models.DateTimeField()
    pettycash_transdescription = models.CharField(max_length=500)
    pettycash_voucherno = models.CharField(max_length=200, null=True, blank=True)
    pettycash_receiptno = models.CharField(max_length=200, null=True, blank=True)
    pettycash_paidby = models.ForeignKey(User, on_delete=models.CASCADE)
    pettycash_account = models.ForeignKey(AccountMaster, on_delete=models.CASCADE)
