from django.db import models

from exams.examtype.models import ExamType
from setups.academics.gradingschemes.models import GradingSchemes
from setups.academics.gradingsystem.models import GradingSystem
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years


class ExamRegistration(models.Model):
    exam_reg_code = models.AutoField(primary_key=True)
    month = models.CharField(max_length=200)
    exam_name = models.CharField(max_length=200,null=True,blank=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    effective_date = models.DateTimeField()
    exam_status = models.BooleanField(default=False)
    final_exam = models.BooleanField(default=False)
    combined_exam = models.BooleanField(default=False)
    exam_national = models.BooleanField(default=False)
    lock_date = models.DateTimeField()
    exam_year = models.ForeignKey(Years,on_delete=models.CASCADE, null=True, blank=True)
    exam_type = models.ForeignKey(ExamType,on_delete=models.CASCADE, null=True, blank=True)
    exam_term = models.ForeignKey(TermDates,on_delete=models.CASCADE, null=True, blank=True)
    exam_grade_scheme = models.ForeignKey(GradingSchemes,on_delete=models.CASCADE, null=True, blank=True)