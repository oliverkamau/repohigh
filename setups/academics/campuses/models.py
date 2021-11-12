from django.db import models

from localities.models import Counties


class Campuses(models.Model):
    campus_code = models.AutoField(primary_key=True)
    campus_name = models.CharField(max_length=200)
    campus_incharge = models.CharField(max_length=200)
    campus_inchargephone = models.CharField(max_length=200)
    campus_location = models.CharField(max_length=200)
    campus_county = models.ForeignKey(Counties, on_delete=models.CASCADE, null=True,blank=True)

