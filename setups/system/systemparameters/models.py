from django.db import models

class SystemParameters(models.Model):
    parameter_code = models.AutoField(primary_key=True)
    parameter_name = models.CharField(max_length=200)
    parameter_desc = models.CharField(max_length=400)
    parameter_status = models.BooleanField(default=True)
    parameter_value = models.CharField(max_length=200)
