from django.urls import include, path

from useradmin import views

urlpatterns = [
	path(r'',views.usersadmin,name='usersadmin'),
	path(r'users/', include('useradmin.users.urls')),
	]