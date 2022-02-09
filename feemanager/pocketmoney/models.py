from django.db import models

from studentmanager.student.models import Students
from useradmin.users.models import User


class PocketMoneyTrans(models.Model):
    pocketmoney_code = models.AutoField(primary_key=True)
    pocketmoney_amount = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    pocketmoney_date = models.DateTimeField()
    pocketmoney_transtype = models.CharField(max_length=200)
    pocketmoney_student = models.ForeignKey(Students, on_delete=models.CASCADE)
    pocketmoney_addedby = models.ForeignKey(User, on_delete=models.CASCADE)
    pocketmoney_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0)