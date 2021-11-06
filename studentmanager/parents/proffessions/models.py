from django.db import models

# Create your models here.
class Proffessions(models.Model):
    proffesion_id = models.AutoField(primary_key=True)
    proffesion_name = models.CharField(max_length=200)
    proffesion_desc = models.CharField(max_length=200)
