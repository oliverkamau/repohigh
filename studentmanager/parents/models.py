from django.db import models

from studentmanager.parents.proffessions.models import Proffessions


class Parents(models.Model):
    parent_code = models.AutoField(primary_key=True)
    father_name = models.CharField(max_length=200,null=True,blank=True)
    mother_name = models.CharField(max_length=200,null=True,blank=True)
    father_address = models.CharField(max_length=200,null=True,blank=True)
    mother_address = models.CharField(max_length=200,null=True,blank=True)
    id_no = models.CharField(max_length=200,null=True,blank=True)
    father_phone = models.CharField(max_length=200,null=True,blank=True)
    mother_phone = models.CharField(max_length=200,null=True,blank=True)
    father_email = models.CharField(max_length=200,null=True,blank=True)
    mother_email = models.CharField(max_length=200,null=True,blank=True)
    parent_type = models.CharField(max_length=200,null=True,blank=True)
    email_required = models.BooleanField(default=True)
    parent_photo=models.ImageField(upload_to='parent_pics',null=True,blank=True)
    father_proffession = models.ForeignKey(Proffessions,related_name='father_proffession_foreignkey', on_delete=models.CASCADE, null=True, blank=True)
    mother_proffession = models.ForeignKey(Proffessions,related_name='mother_proffession_foreignkey', on_delete=models.CASCADE, null=True, blank=True)

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')
