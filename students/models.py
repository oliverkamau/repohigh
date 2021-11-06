from django.db import models

# Create your models here.

class Select2Data(models.Model):
    id: models.CharField(max_length=200)
    text: models.CharField(max_length=255)
    def encode(self):
        return self.__dict__
    class Meta:
         managed = False

class Countries(models.Model):
    country_id= models.AutoField(primary_key=True)
    country_name= models.CharField(max_length=200)
    country_continent= models.CharField(max_length=200)
    country_code= models.CharField(max_length=200)

class Counties(models.Model):
    county_id= models.AutoField(primary_key=True)
    county_name= models.CharField(max_length=200)
    county_code= models.CharField(max_length=200)
    county_country = models.ForeignKey(Countries, on_delete=models.CASCADE)

class StudentDef(models.Model):
    stdCode= models.AutoField(primary_key=True)
    firstName= models.CharField(max_length=200)
    lastName= models.CharField(max_length=200)
    age= models.IntegerField(default=0)
    height= models.IntegerField(default=0)
    stud_country= models.ForeignKey(Countries, on_delete=models.CASCADE,null=True)
    stud_county= models.ForeignKey(Counties, on_delete=models.CASCADE,null=True)
    town= models.CharField(max_length=200)
    phone= models.CharField(max_length=200)
    website= models.CharField(max_length=200)
    photo=models.ImageField(upload_to='parents',null=True)