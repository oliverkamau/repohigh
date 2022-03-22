from django.forms import ModelForm

from timetabling.daysetups.models import DaySetups


class DayForm(ModelForm):
    class Meta:
        model = DaySetups
        fields = '__all__'