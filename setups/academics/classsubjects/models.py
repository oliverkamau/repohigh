from django.db import models

# Create your models here.
from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects


class ClassSubjects(models.Model):
    classsubject_code = models.AutoField(primary_key=True)
    lessons_perweek = models.IntegerField(default=0)
    double_lessons = models.IntegerField(default=0)
    stroked_subject = models.BooleanField(default=False)
    stroked_with = models.IntegerField(default=0)
    classsubject_subject = models.ForeignKey(Subjects,on_delete=models.CASCADE, null=True, blank=True)
    classsubject_class = models.ForeignKey(SchoolClasses,on_delete=models.CASCADE, null=True, blank=True)
