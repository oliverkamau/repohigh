from django.forms import ModelForm

from staff.teachers.models import Teachers


class TeacherForm(ModelForm):

    class Meta:
        model = Teachers
        fields = '__all__'