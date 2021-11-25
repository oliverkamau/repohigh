from django.db import models

# Create your models here.
class Responsibilities(models.Model):
    rb_code = models.AutoField(primary_key=True)
    rb_name = models.CharField(max_length=200)
    rb_ts = models.CharField(max_length=200)