from django.db import models

# Create your models here.
from setups.academics.classes.models import SchoolClasses
from studentmanager.student.models import Students
from useradmin.users.models import User


class Leaveouts(models.Model):
    leave_code = models.AutoField(primary_key=True)
    leave_reason = models.CharField(max_length=500, null=True, blank=True)
    leave_returned = models.CharField(max_length=200, null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    date_expected_back = models.DateTimeField(null=True, blank=True)
    date_left = models.DateTimeField(null=True, blank=True)
    user_returnauthoriser = models.ForeignKey(User, related_name='user_return_foreignkey',on_delete=models.CASCADE, null=True, blank=True)
    user_leaveauthoriser = models.ForeignKey(User, related_name='user_authorised_foreignkey',on_delete=models.CASCADE, null=True, blank=True)
    leave_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE)
    leave_student = models.ForeignKey(Students, on_delete=models.CASCADE)

