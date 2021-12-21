from django.db import models

from feemanager.feesetup.feecategories.models import FeeCategories
from studentmanager.student.models import Students


class BalanceTracker(models.Model):
    tracker_code = models.AutoField(primary_key=True)
    tracker_notes = models.CharField(max_length=600)
    tracker_student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    tracker_date = models.DateTimeField()
    tracker_type = models.CharField(max_length=200,blank=True,null=True)
    tracker_invoiceno = models.CharField(max_length=200,blank=True,null=True)
    structure_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE, null=True, blank=True)