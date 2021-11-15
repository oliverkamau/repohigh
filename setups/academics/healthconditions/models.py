from django.db import models

class HealthStatus(models.Model):
    healthcondition_code = models.AutoField(primary_key=True)
    healthcondition_name = models.CharField(max_length=200)
    healthcondition_desc = models.CharField(max_length=400,null=True,blank=True)