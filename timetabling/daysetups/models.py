from django.db import models

class DaySetups(models.Model):
    day_code = models.AutoField(primary_key=True)
    day_name = models.CharField(max_length=200)