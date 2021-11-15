from django.db import models

from staff.teachers.models import Teachers


class SchoolClasses(models.Model):
    class_code = models.AutoField(primary_key=True)
    form = models.CharField(max_length=200)
    stream = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    active=models.BooleanField(default=True)
    max_capacity=models.IntegerField(default=0)
    admno_prefix = models.CharField(max_length=200,null=True,blank=True)
    class_teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True,blank=True)
    next_class = models.ForeignKey("self", on_delete=models.CASCADE, null=True,blank=True)