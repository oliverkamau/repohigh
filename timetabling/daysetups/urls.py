from django.urls import path

from . import views

urlpatterns = [

	path(r'daysetups', views.daysetups,name="daysetups"),
	path(r'createday', views.createday, name="createday"),
	path(r'getdays', views.getdays, name="getdays"),
	path(r'getdays', views.getdays, name="getdays"),
	path(r'editday/<int:id>', views.editday, name="editday"),
	path(r'deleteday/<int:id>', views.deleteday, name="deleteday"),
	path(r'updateday/<int:id>', views.updateday, name="updateday"),


]