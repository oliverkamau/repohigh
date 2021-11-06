from django.forms import ModelForm

from useradmin.users.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'