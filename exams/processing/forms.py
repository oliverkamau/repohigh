from django.forms import ModelForm

from exams.processing.models import ExamProcessing


class ProcessingForm(ModelForm):
    class Meta:
        model = ExamProcessing
        fields = '__all__'