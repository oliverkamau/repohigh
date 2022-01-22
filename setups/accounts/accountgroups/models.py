from django.db import models

# Create your models here.
class AccountGroups(models.Model):
    accountgroup_id = models.AutoField(primary_key=True)
    accountgroup_code = models.CharField(max_length=200)
    accountgroup_serial = models.CharField(max_length=200)
    accountgroup_name = models.CharField(max_length=400)
