from django.urls import path,include

from setups import views

urlpatterns = [
	path(r'academicsetups', views.academics, name="academics"),
	path(r'academics/', include('setups.academics.urls')),
	path(r'organization/', include('setups.organization.urls'))

]