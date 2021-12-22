from django.db import models

from setups.academics.departments.models import Departments


class SystemSequences(models.Model):
    sequence_code = models.AutoField(primary_key=True)
    sequence_type = models.CharField(max_length=200)
    sequence_nextseq = models.BigIntegerField(default=0)
    sequence_department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True,blank=True)
