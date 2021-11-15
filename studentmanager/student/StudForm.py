from django.core.exceptions import ValidationError
from django.forms import ModelForm

from studentmanager.student.models import Students


class StudForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("student_name")

        if name == '':
                raise ValidationError(
                    "Form Student Name Not Availed"
                )
    class Meta:
        model = Students
        fields = '__all__'
