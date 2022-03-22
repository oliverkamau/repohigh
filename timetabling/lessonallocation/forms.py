from django.forms import ModelForm

from timetabling.lessonallocation.models import LessonAllocation


class LessonAllocationForm(ModelForm):
    class Meta:
        model = LessonAllocation
        fields = '__all__'

