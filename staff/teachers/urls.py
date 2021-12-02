from django.urls import path

from . import views

urlpatterns = [

    path('teacherpage', views.teacherpage, name='teacherpage'),
    path('dynamicaddress',views.dynamicaddress, name='dynamicaddress'),
    path('searchtitle', views.searchtitle, name='searchtitle'),
    path('searchresponsibility', views.searchresponsibility, name='searchresponsibility'),
    path('searchdepartment', views.searchdepartment, name='searchdepartment'),
    path('addteachers', views.addteachers, name='addteachers'),
    path('getteachers', views.getteachers, name='getteachers'),
    path('editteacher/<int:id>', views.editteacher, name='editteacher'),
    path('deleteteacher/<int:id>', views.deleteteacher, name='deleteteacher'),
    path('updateteachers/<int:id>', views.updateteachers, name='updateteachers'),
    path('getassignedsubjects/<int:id>/<int:cl>', views.getassignedsubjects, name='getassignedsubjects'),
    path('getunassignedsubjects/<int:id>/<int:cl>', views.getunassignedsubjects, name='getunassignedsubjects'),
    path('assignsubjects', views.assignsubjects, name='assignsubjects'),
    path('unassignsubjects', views.unassignsubjects, name='unassignsubjects'),
    path('unassignallsubjects', views.unassignallsubjects, name='unassignallsubjects'),
    path('assignallsubjects', views.assignallsubjects, name='assignallsubjects'),
    path('searchteachers', views.searchteachers, name='searchteachers'),
    path('transfersubjects', views.transfersubjects, name='transfersubjects'),
    path('searchclasses', views.searchclasses, name='searchclasses'),

]
