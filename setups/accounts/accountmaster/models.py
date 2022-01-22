from django.db import models

# Create your models here.
from setups.accounts.accountgroups.models import AccountGroups


class AccountMaster(models.Model):
    account_id = models.AutoField(primary_key=True)
    accountsub_code = models.CharField(max_length=200)
    account_no = models.CharField(max_length=200)
    account_serial = models.CharField(max_length=200)
    account_order = models.IntegerField(default=0)
    account_main = models.CharField(max_length=200)
    account_name = models.CharField(max_length=400)
    account_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    account_status = models.BooleanField(default=True)
    account_drcr = models.CharField(max_length=200,blank=True,null=True)
    account_reconcile = models.CharField(max_length=200,blank=True,null=True)
    account_restrictpost = models.CharField(max_length=200,blank=True,null=True)
    account_cashbook = models.CharField(max_length=200,blank=True,null=True)
    account_trialbalance = models.CharField(max_length=200,blank=True,null=True)
    account_tradingaccount = models.CharField(max_length=200,blank=True,null=True)
    account_balancesheet = models.CharField(max_length=200,blank=True,null=True)
    account_incomeexpenditure = models.CharField(max_length=200,blank=True,null=True)
    account_profitloss = models.CharField(max_length=200,blank=True,null=True)
    account_pettycash = models.CharField(max_length=200,blank=True,null=True)
    account_mainaccount = models.ForeignKey("self", on_delete=models.CASCADE, null=True,blank=True)
    account_accountgroup = models.ForeignKey(AccountGroups,on_delete=models.CASCADE)
