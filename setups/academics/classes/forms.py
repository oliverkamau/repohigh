from django.forms import ModelForm

from setups.academics.classes.models import SchoolClasses


class ClassForm(ModelForm):
    class Meta:
        model = SchoolClasses
        fields = '__all__'