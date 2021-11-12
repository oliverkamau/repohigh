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
from studentmanager.parents.models import Parents


class Students(models.Model):
      student_code = models.AutoField(primary_key=True)
      adm_no = models.CharField(max_length=200)
      student_upi = models.CharField(max_length=200)
      student_name = models.CharField(max_length=200)
      student_gender = models.CharField(max_length=200)
      adm_term = models.CharField(max_length=200)
      student_address = models.CharField(max_length=200)
      student_email = models.CharField(max_length=200)
      parent_phone = models.CharField(max_length=200)
      student_phone = models.CharField(max_length=200)
      adm_date = models.DateTimeField()
      date_of_birth = models.DateTimeField()
      completion_date = models.DateTimeField()
      birth_cert_no = models.CharField(max_length=200)
      index_no = models.CharField(max_length=200)
      marks = models.CharField(max_length=200)
      grade = models.CharField(max_length=200)
      primary_school = models.CharField(max_length=200)
      student_photo = models.ImageField(upload_to="studentphoto",null=True,blank=True)
      student_fee_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE, null=True)
      student_dorm = models.ForeignKey(Dorms, on_delete=models.CASCADE, null=True)
      student_campus = models.ForeignKey(Campuses, on_delete=models.CASCADE, null=True)
      student_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE, null=True)
      student_parent = models.ForeignKey(Parents, on_delete=models.CASCADE, null=True)
      nationality = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True)
      student_county = models.ForeignKey(Counties, on_delete=models.CASCADE, null=True)
      stud_sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, null=True)
      stud_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
      stud_sub_location = models.ForeignKey(SubLocation, on_delete=models.CASCADE, null=True)
      stud_village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
      student_denomination = models.ForeignKey(Denomination, on_delete=models.CASCADE, null=True)
      student_sources = models.ForeignKey(StudentSources, on_delete=models.CASCADE, null=True)
      health_status = models.ForeignKey(HealthStatus, on_delete=models.CASCADE, null=True)
      student_status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE, null=True)