from django.db import models

class StudentStatus(models.Model):
    status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=200)
    status_desc = models.CharField(max_length=200,null=True,blank=True)