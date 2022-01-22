from django.db import models

# Create your models here.
from setups.accounts.accountmaster.models import AccountMaster
from useradmin.users.models import User


class FloatReplenishment(models.Model):
    float_code = models.AutoField(primary_key=True)
    float_amount = models.DecimalField(max_digits=13, decimal_places=2)
    float_docno = models.CharField(max_length=200,blank=True,null=True)
    float_date = models.DateTimeField()
    float_runningbalance = models.DecimalField(max_digits=13, decimal_places=2,default=0)
    float_assignee = models.ForeignKey(User,related_name='float_assignee_foreignkey',on_delete=models.CASCADE)
    float_assigner = models.ForeignKey(User,related_name='float_assigner_foreignkey',on_delete=models.CASCADE)
    float_account = models.ForeignKey(AccountMaster,on_delete=models.CASCADE)
