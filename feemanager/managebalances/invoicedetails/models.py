from django.db import models

from feemanager.managebalances.singleinvoicing.models import BalanceTracker
from setups.accounts.standardcharges.models import StandardCharges


class BalanceTrackerDetails(models.Model):
    trackerdetails_code = models.AutoField(primary_key=True)
    trackerdetails_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    trackerdetails_Standardcharge = models.ForeignKey(StandardCharges, on_delete=models.CASCADE)
    trackerdetails_tracker = models.ForeignKey(BalanceTracker, on_delete=models.CASCADE)