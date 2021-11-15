from django.db import models

class Documents(models.Model):
    document_code = models.AutoField(primary_key=True)
    document_name = models.CharField(max_length=200,blank=True,null=True)
    document_desc = models.CharField(max_length=200,null=True,blank=True)
    document_required = models.BooleanField(default=False)