from django.forms import ModelForm
from .models import StudentDef, Countries, Counties

class CountriesForm(ModelForm):
    class Meta:
        model = Countries
        fields = '__all__'

class CountiesForm(ModelForm):
    class Meta:
        model = Counties
        fields = '__all__'
        
class StudentForm(ModelForm):
    class Meta:
        model = StudentDef
        fields = '__all__'