from django.urls import include, path

urlpatterns = [
	path(r'teachers/', include('staff.teachers.urls'))

]