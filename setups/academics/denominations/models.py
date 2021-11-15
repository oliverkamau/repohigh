from django.db import models

# Create your models here.
class Denomination(models.Model):
    denomination_code = models.AutoField(primary_key=True)
    denomination_name = models.CharField(max_length=200,null=True,blank=True)
    denomination_day = models.CharField(max_length=200,null=True,blank=True)