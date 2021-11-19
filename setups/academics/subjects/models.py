from django.db import models

from setups.academics.models import Departments


class Subjects(models.Model):
    subject_code = models.AutoField(primary_key=True)
    subject_order = models.CharField(max_length=200)
    subject_sht_desc = models.CharField(max_length=200,null=True,blank=True)
    subject_name = models.CharField(max_length=200)
    main_subject = models.BooleanField(default=False)
    combined_subject = models.BooleanField(default=False)
    include_for_pos = models.BooleanField(default=False)
    subject_multiplier = models.CharField(max_length=200,null=True,blank=True)
    timetable_name = models.CharField(max_length=200,null=True,blank=True)
    mandatory_subject = models.BooleanField(default=False)
    subject_department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True,blank=True)

