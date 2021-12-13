from django.db import models

from exams.registration.models import ExamRegistration
from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
from staff.teachers.models import Teachers
from studentmanager.student.models import Students
from useradmin.users.models import User


class ExamProcessing(models.Model):
    exam_process_code = models.AutoField(primary_key=True)
    exam_marks = models.CharField(max_length=200,null=True,blank=True)
    exam_outof = models.CharField(max_length=200,null=True,blank=True)
    exam_processing_grade = models.CharField(max_length=200,null=True,blank=True)
    exam_process_date = models.DateTimeField()
    exam_percentage_marks = models.CharField(max_length=200,null=True,blank=True)
    position_outof = models.CharField(max_length=200,null=True,blank=True)
    position_persubject = models.CharField(max_length=200,null=True,blank=True)
    position_perclass = models.CharField(max_length=200, null=True, blank=True)
    overall_marks = models.CharField(max_length=200, null=True, blank=True)
    overall_grade = models.CharField(max_length=200,null=True,blank=True)
    overall_position=models.CharField(max_length=200, null=True, blank=True)
    overall_outof=models.CharField(max_length=200, null=True, blank=True)
    stream_position = models.CharField(max_length=200, null=True, blank=True)
    stream_positionoutof=models.CharField(max_length=200, null=True, blank=True)
    class_mean_grade = models.CharField(max_length=200, null=True, blank=True)
    class_mean_mark =  models.CharField(max_length=200, null=True, blank=True)
    form_mean_grade = models.CharField(max_length=200, null=True, blank=True)
    form_mean_mark = models.CharField(max_length=200, null=True, blank=True)
    exam_process_remarks = models.CharField(max_length=400,null=True,blank=True)
    exam_process_exam = models.ForeignKey(ExamRegistration,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_term = models.ForeignKey(TermDates,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_class = models.ForeignKey(SchoolClasses,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_teacher = models.ForeignKey(Teachers,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_subject = models.ForeignKey(Subjects,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_student = models.ForeignKey(Students,on_delete=models.CASCADE, null=True, blank=True)
    exam_process_year = models.ForeignKey(Years,on_delete=models.CASCADE, null=True, blank=True)
    exam_processed_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)



class MarksExcelFile(models.Model):
    file = models.FileField(upload_to='marksexcel')