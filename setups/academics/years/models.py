from django.db import models

class Years(models.Model):
    year_code = models.AutoField(primary_key=True)
    year_name = models.CharField(max_length=200)
    year_number = models.IntegerField(default=0)
