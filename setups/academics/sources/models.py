from django.db import models

from feemanager.feesetup.feecategories.models import FeeCategories


class StudentSources(models.Model):
    studentsources_code = models.AutoField(primary_key=True)
    studentsources_name = models.CharField(max_length=200)
    studentsources_desc = models.CharField(max_length=200)
