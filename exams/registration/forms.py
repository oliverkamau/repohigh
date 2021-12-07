from django.forms import ModelForm

from exams.registration.models import ExamRegistration


class ExamRegForm(ModelForm):
    class Meta:
        model = ExamRegistration
        fields = '__all__'