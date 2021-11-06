from django.forms import ModelForm

from setups.academics.termdates.models import TermDates


class TermForm(ModelForm):
    class Meta:
        model = TermDates
        fields = '__all__'