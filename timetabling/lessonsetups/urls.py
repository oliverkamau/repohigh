from django.urls import path

from . import views

urlpatterns = [

	path(r'lessonsetup', views.lessonsetup,name="lessonsetup"),
    path(r'createlesson', views.createlesson, name="createlesson"),
	path(r'getlessons', views.getlessons, name="getlessons"),
	path(r'editlesson/<int:id>', views.editlesson, name="editlesson"),
	path(r'deletelesson/<int:id>', views.deletelesson, name="deletelesson"),
	path(r'updatelesson/<int:id>', views.updatelesson, name="updatelesson"),

]