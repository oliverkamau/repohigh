from django.db import models

# Create your models here.
class Departments(models.Model):
    dp_code = models.AutoField(primary_key=True)
    dp_name = models.CharField(max_length=200)
    dp_short_desc = models.CharField(max_length=200)
    seq_desc = models.CharField(max_length=200)