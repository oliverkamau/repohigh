from django.db import models

from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates


class DoublesTracker(models.Model):
    doubletracker_code = models.AutoField(primary_key=True)
    doubletracker_subject = models.ForeignKey(Subjects, on_delete=models.CASCADE,null=True)
    doubletracker_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE,null=True)
    doubletracker_term = models.ForeignKey(TermDates, on_delete=models.CASCADE,null=True)
    doubletracker_number = models.IntegerField(default=0)
