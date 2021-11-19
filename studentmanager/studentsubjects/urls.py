from django.urls import path

from studentmanager.studentsubjects import views

urlpatterns = [
    path('getstudentsubject', views.getstudentsubject, name='getstudentsubject'),
    path('searchclasses', views.searchclasses, name='searchclasses'),
    path('searchsubjects', views.searchsubjects, name='searchsubjects'),
    path('getunassignedstudents/<int:classcode>/<int:subject>', views.getunassignedstudents, name='getunassignedstudents'),
    path('getassignedstudents/<int:classcode>/<int:subject>', views.getassignedstudents, name='getassignedstudents'),
    path('assignsubjects', views.assignsubjects, name='assignsubjects'),
    path('unassignsubjects', views.unassignsubjects, name='unassignsubjects'),
    path('assignallsubjects', views.assignallsubjects, name='assignallsubjects'),
    path('unassignallsubjects', views.unassignallsubjects, name='unassignallsubjects'),
    path('dynamicaddress', views.dynamicaddress, name='dynamicaddress'),
    path('populatemandatorysubjects', views.populatemandatorysubjects, name='populatemandatorysubjects'),

]