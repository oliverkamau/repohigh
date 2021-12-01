from django.db import models

# Create your models here.
from setups.academics.subjects.models import Subjects
from staff.teachers.models import Teachers


class TeacherSubjects(models.Model):
    teacher_subjectcode = models.AutoField(primary_key=True)
    teacher_subjectteacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True, blank=True)
    teacher_subjectsubject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)
