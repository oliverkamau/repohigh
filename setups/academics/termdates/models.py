from django.db import models

from setups.academics.classes.models import SchoolClasses


class TermDates(models.Model):
    term_code = models.AutoField(primary_key=True)
    term_number = models.CharField(max_length=200)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    current_term = models.BooleanField(default=True)
    term_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE, null=True, blank=True)