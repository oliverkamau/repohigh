from django.db import models

from feemanager.feesetup.feecategories.models import FeeCategories
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
from setups.accounts.standardcharges.models import StandardCharges



class FeeStructure(models.Model):
    structure_code = models.AutoField(primary_key=True)
    structure_year = models.ForeignKey(Years, on_delete=models.CASCADE, null=True, blank=True)
    structure_term = models.ForeignKey(TermDates, on_delete=models.CASCADE, null=True, blank=True)
    structure_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE, null=True, blank=True)
