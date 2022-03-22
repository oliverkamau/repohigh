from django.urls import path

from . import views

urlpatterns = [

	path(r'lessonallocation', views.lessonallocation,name="lessonallocation"),
	path(r'searchclasses', views.searchclasses, name="searchclasses"),
	path(r'searchdays', views.searchdays, name="searchdays"),
	path(r'searchlessons', views.searchlessons, name="searchlessons"),
	path(r'searchteachers', views.searchteachers, name="searchteachers"),
	path(r'searchsubjects', views.searchsubjects, name="searchsubjects"),
	path(r'getcurrentterm', views.getcurrentterm, name="getcurrentterm"),
	path(r'getTimetable', views.getTimetable, name="getTimetable"),
	path(r'createtimetable', views.createtimetable, name="createtimetable"),
	path(r'updatetimetable/<int:id>', views.updatetimetable, name="updatetimetable"),
	path(r'getteacher/<int:classcodes>/<int:subject>', views.getteacher, name="getteacher"),

]