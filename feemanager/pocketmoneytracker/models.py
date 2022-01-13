from django.db import models

from studentmanager.student.models import Students


class PocketMoneyTracker(models.Model):
    tracker_code = models.AutoField(primary_key=True)
    tracker_student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    tracker_date = models.DateTimeField()
    tracker_invoiceno = models.CharField(max_length=200, blank=True, null=True)
    tracker_balance = models.DecimalField(max_digits=13, decimal_places=2, default=0)