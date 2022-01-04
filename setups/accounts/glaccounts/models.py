from django.db import models

class GlAccounts(models.Model):
    glaccount_code = models.AutoField(primary_key=True)
    glaccount_name = models.CharField(max_length=200, null=True, blank=True)
    glaccount_desc = models.CharField(max_length=400, null=True, blank=True)
    glaccount_no = models.CharField(max_length=200, null=True, blank=True)



