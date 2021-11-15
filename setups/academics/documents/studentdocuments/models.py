from django.db import models

from setups.academics.documents.models import Documents
from studentmanager.student.models import Students


class StudentDocument(models.Model):
    stud_doc_code = models.AutoField(primary_key=True)
    document_file = models.FileField(upload_to='studentdocs', null=True,blank=True)
    stud_doc_student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    stud_doc_document = models.ForeignKey(Documents, on_delete=models.CASCADE, null=True)


