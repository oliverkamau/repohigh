import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.http import JsonResponse
from rest_framework import status


class UserType(models.Model):
    type_code = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=200)
    type_desc = models.CharField(max_length=200)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password,user_firstname,user_lastname,email,user_phone,
                    user_address,user_gender,user_active,user_teacher_ref,user_type,user_supervisor):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username,user_firstname=user_firstname,user_lastname=user_lastname,email=email,user_phone=user_phone,
                    user_address=user_address,user_gender=user_gender,is_active=user_active,user_teacher_ref=user_teacher_ref,user_type=user_type,user_supervisor=user_supervisor)
        user.set_password(password)


        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'username already taken'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            user.save(using=self._db)
            return user


class User(AbstractBaseUser,models.Model):
    user_id = models.AutoField(primary_key=True)
    user_firstname = models.CharField(max_length=200,null=True,blank=True)
    user_lastname = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200,unique=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    user_phone = models.CharField(max_length=200,null=True,blank=True)
    user_address = models.CharField(max_length=200,null=True,blank=True)
    user_gender = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateField(verbose_name="date_created",default=datetime.date.today)
    last_login = models.DateField(verbose_name="last_login",auto_now=True)
    is_active = models.BooleanField(default=True)
    user_teacher_ref = models.IntegerField(default=0,blank=True,null=True)
    user_type= models.ForeignKey(UserType, on_delete=models.CASCADE,null=True)
    user_supervisor= models.ForeignKey("self", on_delete=models.CASCADE,null=True)
    password = models.CharField(max_length=200,null=True,blank=True,default=None)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

