from django.db import models

from setups.academics.models import Departments, Responsibilities
from useradmin.users.models import User


class TeacherSalution(models.Model):
    salutation_id = models.AutoField(primary_key=True)
    salutation_name = models.CharField(max_length=200)
    salutation_desc = models.CharField(max_length=200)

class Teachers(models.Model):
    teacher_code= models.AutoField(primary_key=True)
    teacher_name= models.CharField(max_length=200)
    box_address= models.CharField(max_length=200)
    phone_number= models.CharField(max_length=200)
    staff_number= models.CharField(max_length=200)
    date_joined = models.DateTimeField()
    date_left= models.DateTimeField()
    gender= models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    intials=models.CharField(max_length=200)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    id_no=models.CharField(max_length=200)
    finger_print=models.BinaryField()
    finger_print_date=models.DateTimeField();
    finger_print_user=models.CharField(max_length=200)
    tsc_no=models.CharField(max_length=200)
    teacher_pic=models.BinaryField()
    department= models.ForeignKey(Departments, on_delete=models.CASCADE,null=True)
    responsibility= models.ForeignKey(Responsibilities, on_delete=models.CASCADE,null=True)
    title = models.ForeignKey(TeacherSalution, on_delete=models.CASCADE, null=True)
