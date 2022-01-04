from django.db import models

from setups.accounts.banks.models import Banks
from setups.accounts.glaccounts.models import GlAccounts


class BankBranches(models.Model):
    bankbranch_code = models.AutoField(primary_key=True)
    bankbranch_name = models.CharField(max_length=200, null=True, blank=True)
    bankbranch_accountname = models.CharField(max_length=200, null=True, blank=True)
    bankbranch_accountnumber = models.CharField(max_length=200, null=True, blank=True)
    bankbranch_bank = models.ForeignKey(Banks,on_delete=models.CASCADE)
    bankbranch_glname = models.ForeignKey(GlAccounts,on_delete=models.CASCADE)

