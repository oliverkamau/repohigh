from django.forms import ModelForm

from setups.academics.documents.studentdocuments.models import StudentDocument


class StudentDocsForm(ModelForm):

    class Meta:
        model = StudentDocument
        fields = '__all__'