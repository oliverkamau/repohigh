from django.db import models

class LessonSetups(models.Model):
    lesson_code = models.AutoField(primary_key=True)
    lesson_name = models.CharField(max_length=200)
    lesson_start = models.DateTimeField()
    lesson_end = models.DateTimeField()
    lesson_duration = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=200,null=True,blank=True)
    lesson_auto = models.BooleanField(default=True)