from django.db import models

class ExamType(models.Model):
    type_code = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=200)
    type_desc = models.CharField(max_length=400, null=True, blank=True)

