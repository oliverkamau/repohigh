from django.db import models

from setups.academics.departments.models import Departments
from setups.academics.responsibilities.models import Responsibilities
from useradmin.users.models import User


class TeacherSalution(models.Model):
    salutation_id = models.AutoField(primary_key=True)
    salutation_name = models.CharField(max_length=200)
    salutation_desc = models.CharField(max_length=200)

class Teachers(models.Model):
    teacher_code= models.AutoField(primary_key=True)
    teacher_name= models.CharField(max_length=200)
    box_address= models.CharField(max_length=200,blank=True,null=True)
    phone_number= models.CharField(max_length=200,blank=True,null=True)
    staff_number= models.CharField(max_length=200,blank=True,null=True)
    date_joined = models.DateTimeField(blank=True,null=True)
    date_left= models.DateTimeField(blank=True,null=True)
    gender= models.CharField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    status=models.CharField(max_length=200,blank=True,null=True)
    intials=models.CharField(max_length=200,blank=True,null=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    id_no=models.CharField(max_length=200,blank=True,null=True)
    finger_print=models.BinaryField(blank=True,null=True)
    finger_print_date=models.DateTimeField(blank=True,null=True);
    finger_print_user=models.CharField(max_length=200,blank=True,null=True)
    tsc_no=models.CharField(max_length=200,blank=True,null=True)
    teacher_pic=models.ImageField(upload_to='teacher-pics',blank=True,null=True)
    department= models.ForeignKey(Departments, on_delete=models.CASCADE,null=True,blank=True)
    responsibility= models.ForeignKey(Responsibilities, on_delete=models.CASCADE,blank=True,null=True)
    title = models.ForeignKey(TeacherSalution, on_delete=models.CASCADE, blank=True,null=True)
