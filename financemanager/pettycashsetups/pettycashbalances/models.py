from django.db import models

# Create your models here.
from useradmin.users.models import User


class PettyCashBalances(models.Model):
    pettycashbalance_code = models.AutoField(primary_key=True)
    pettycashbalance_amount = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    pettycashbalance_user = models.ForeignKey(User, on_delete=models.CASCADE)
