from django.urls import path

from schoolsys.views import custom404
from useradmin.users import views
handler404 = custom404
urlpatterns = [
	path(r'userreg', views.userreg, name="userreg"),
    path(r'createuser', views.createuser, name="createuser"),
    path(r'updateuser/<int:id>', views.updateuser, name="updateuser"),
    path(r'editusers/<int:id>', views.edituser, name="edituser"),
    path(r'deleteuser/<int:id>', views.deleteuser, name="deleteuser"),
    path(r'getusers', views.getusers, name="getusers"),
    path(r'searchtypes', views.searchtypes, name="searchtypes"),
    path(r'searchsupervisor', views.searchsupervisor, name="searchsupervisor"),
    path(r'searchteachers', views.searchteachers, name="searchteachers")

]