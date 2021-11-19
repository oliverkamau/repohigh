from django.db import models

# Create your models here.
from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects
from studentmanager.student.models import Students


class StudentSubjects(models.Model):
    stud_subject_code = models.AutoField(primary_key=True)
    stud_subject_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE, null=True,blank=True)
    stud_subject_student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True,blank=True)
    stud_subject_subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True,blank=True)

