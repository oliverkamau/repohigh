from django.db import models

from setups.academics.departments.models import Departments
from setups.academics.gradingschemes.models import GradingSchemes


class GradesApplicableTo(models.Model):
    applicable_code = models.AutoField(primary_key=True)
    applicable_name = models.CharField(max_length=200)

class GradingSystem(models.Model):
    grading_code = models.AutoField(primary_key=True)
    grading_name = models.CharField(max_length=200)
    points_from = models.CharField(max_length=200, null=True, blank=True)
    points_to = models.CharField(max_length=200, null=True, blank=True)
    grading_grade = models.CharField(max_length=200, null=True, blank=True)
    grading_remarks = models.CharField(max_length=400, null=True, blank=True)
    auto_increment = models.BooleanField(default=False)
    default_system = models.BooleanField(default=False)
    applicable_for = models.ForeignKey(GradesApplicableTo, on_delete=models.CASCADE, null=True, blank=True)
    grading_department = models.ForeignKey(Departments,on_delete=models.CASCADE, null=True, blank=True)
    grading_scheme = models.ForeignKey(GradingSchemes,on_delete=models.CASCADE, null=True, blank=True)
