from django.db import models

class Banks(models.Model):
    bank_code = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
