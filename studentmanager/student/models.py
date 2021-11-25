from django.db import models

from feemanager.feesetup.feecategories.models import FeeCategories
from localities.models import Countries, Counties, Location, SubLocation, SubCounty, Village
from setups.academics.campuses.models import Campuses
from setups.academics.classes.models import SchoolClasses
from setups.academics.denominations.models import Denomination
from setups.academics.dorms.models import Dorms
from setups.academics.healthconditions.models import HealthStatus
from setups.academics.sources.models import StudentSources
from setups.academics.studentstatus.models import StudentStatus
from setups.academics.years.models import Years
from studentmanager.parents.models import Parents


class Students(models.Model):
      student_code = models.AutoField(primary_key=True)
      adm_no = models.CharField(max_length=200,null=True,blank=True)
      student_upi = models.CharField(max_length=200,null=True,blank=True)
      student_name = models.CharField(max_length=200,null=True,blank=True)
      student_gender = models.CharField(max_length=200,null=True,blank=True)
      adm_term = models.CharField(max_length=200,null=True,blank=True)
      student_address = models.CharField(max_length=200,null=True,blank=True)
      student_email = models.CharField(max_length=200,null=True,blank=True)
      parent_phone = models.CharField(max_length=200,null=True,blank=True)
      student_phone = models.CharField(max_length=200,null=True,blank=True)
      adm_date = models.DateTimeField(null=True,blank=True)
      date_of_birth = models.DateTimeField(null=True,blank=True)
      completion_date = models.DateTimeField(null=True,blank=True)
      birth_cert_no = models.CharField(max_length=200,null=True,blank=True)
      index_no = models.CharField(max_length=200,null=True,blank=True)
      marks = models.CharField(max_length=200,null=True,blank=True)
      grade = models.CharField(max_length=200,null=True,blank=True)
      primary_school = models.CharField(max_length=200,null=True,blank=True)
      student_photo = models.ImageField(upload_to="studentphoto",null=True,blank=True)
      student_school_status= models.CharField(max_length=200,blank=True,default='Active')
      student_statuschange_date = models.DateTimeField(null=True,blank=True)
      student_resume_date = models.DateTimeField(null=True,blank=True)
      student_statuschange_term = models.CharField(max_length=200,null=True,blank=True)
      student_statuschange_reason = models.CharField(max_length=500,blank=True,null=True)
      year_of_completion = models.CharField(max_length=200,blank=True,null=True)
      student_fee_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE, null=True,blank=True)
      student_dorm = models.ForeignKey(Dorms, on_delete=models.CASCADE, null=True,blank=True)
      student_campus = models.ForeignKey(Campuses, on_delete=models.CASCADE, null=True,blank=True)
      student_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE, null=True,blank=True)
      student_parent = models.ForeignKey(Parents, on_delete=models.CASCADE, null=True,blank=True)
      nationality = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True,blank=True)
      student_county = models.ForeignKey(Counties, on_delete=models.CASCADE, null=True,blank=True)
      stud_sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, null=True,blank=True)
      stud_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True,blank=True)
      stud_sub_location = models.ForeignKey(SubLocation, on_delete=models.CASCADE, null=True,blank=True)
      stud_village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True,blank=True)
      student_denomination = models.ForeignKey(Denomination, on_delete=models.CASCADE, null=True,blank=True)
      student_sources = models.ForeignKey(StudentSources, on_delete=models.CASCADE, null=True,blank=True)
      health_status = models.ForeignKey(HealthStatus, on_delete=models.CASCADE, null=True,blank=True)
      student_status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE, null=True,blank=True)
      student_exam_year = models.ForeignKey(Years, on_delete=models.CASCADE, null=True,blank=True)
