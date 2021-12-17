from django.db import models

from feemanager.feesetup.feestructure.models import FeeStructure
from setups.accounts.standardcharges.models import StandardCharges


class FeeStructureDetails(models.Model):
    structuredetail_code = models.AutoField(primary_key=True)
    structuredetail_ammount = models.DecimalField(max_digits=13,decimal_places=2,default=0)
    structuredetail_Standardcharge = models.ForeignKey(StandardCharges, on_delete=models.CASCADE)
    structuredetail_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
