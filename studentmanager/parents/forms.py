from django.forms import ModelForm

from studentmanager.parents.models import Parents


class ParentsForm(ModelForm):
    class Meta:
        model = Parents
        fields = '__all__'