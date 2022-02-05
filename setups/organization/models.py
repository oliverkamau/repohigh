from django.db import models

# Create your models here.
class Organization(models.Model):
    organization_code = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=200, null=True, blank=True)
    physical_address = models.CharField(max_length=400, null=True, blank=True)
    postal_address = models.CharField(max_length=400, null=True, blank=True)
    organization_telno = models.CharField(max_length=200, null=True, blank=True)
    organization_cellno = models.CharField(max_length=200, null=True, blank=True)
    organization_mission = models.CharField(max_length=400, null=True, blank=True)
    organization_vision= models.CharField(max_length=400, null=True, blank=True)
    organization_motto= models.CharField(max_length=400, null=True, blank=True)
    organization_websites = models.CharField(max_length=200, null=True, blank=True)
    organization_email = models.CharField(max_length=200, null=True, blank=True)
    organization_logo = models.ImageField(upload_to="orglogos", null=True, blank=True)
