from django.forms import ModelForm

from timetabling.lessonsetups.models import LessonSetups


class LessonForm(ModelForm):
    class Meta:
        model = LessonSetups
        fields = '__all__'