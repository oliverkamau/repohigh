from django.db import models

class Dorms(models.Model):
    dorm_code = models.AutoField(primary_key=True)
    dorm_name = models.CharField(max_length=200)
    max_capacity=models.IntegerField(default=0)


