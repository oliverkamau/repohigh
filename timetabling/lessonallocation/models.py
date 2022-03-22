from django.db import models

# Create your models here.
from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates
from staff.teachers.models import Teachers
from timetabling.daysetups.models import DaySetups
from timetabling.lessonsetups.models import LessonSetups


class LessonAllocation(models.Model):
    timetable_code = models.AutoField(primary_key=True)
    timetable_day = models.ForeignKey(DaySetups, on_delete=models.CASCADE,null=True)
    timetable_lesson = models.ForeignKey(LessonSetups, on_delete=models.CASCADE,null=True)
    timetable_class =  models.ForeignKey(SchoolClasses, on_delete=models.CASCADE,null=True)
    timetable_subject =  models.ForeignKey(Subjects, on_delete=models.CASCADE,null=True)
    timetable_term = models.ForeignKey(TermDates, on_delete=models.CASCADE,null=True)
    timetable_teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE,null=True)

