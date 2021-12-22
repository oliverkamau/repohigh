from django.db import models

class InvoiceSequence(models.Model):
    sequence_code = models.AutoField(primary_key=True)
    sequence_no = models.BigIntegerField(default=0,null=True, blank=True)