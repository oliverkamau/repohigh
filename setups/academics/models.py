from django.db import models

from useradmin.users.models import UserType


class Responsibilities(models.Model):
    rb_code = models.AutoField(primary_key=True)
    rb_name = models.CharField(max_length=200)
    rb_ts = models.CharField(max_length=200)

class Departments(models.Model):
    dp_code = models.AutoField(primary_key=True)
    dp_name = models.CharField(max_length=200)
    dp_short_desc = models.CharField(max_length=200)
    seq_desc = models.CharField(max_length=200)

