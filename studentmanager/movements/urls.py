from django.urls import path

from studentmanager.movements import views

urlpatterns = [
    path('studentmovements', views.studentmovements, name='studentmovements'),
    path('searchclasses', views.searchclasses, name='searchclasses'),
    path('searchtableclasses', views.searchclasses, name='searchtableclasses'),
    path('searchstudent/<int:id>', views.searchstudent, name='searchstudent'),
    path('getspecificstudents/<str:action>', views.getspecificstudents, name='getspecificstudents'),
    path('getstudents', views.getstudents, name='getstudents'),
    path('getunassignedstudents/<int:id>', views.getunassignedstudents,
         name='getunassignedstudents'),
    path('getassignedstudents/<int:id>', views.getassignedstudents, name='getassignedstudents'),
    path('dynamicaddress', views.dynamicaddress, name='dynamicaddress'),
    path('studentmovement', views.studentmovement, name='studentmovement'),
    path('assignstudents', views.assignstudents, name='assignstudents'),
    path('unassignstudents', views.unassignstudents, name='unassignstudents'),
    path('assignallstudents', views.assignallstudents, name='assignallstudents'),
    path('unassignallstudents', views.unassignallstudents, name='unassignallstudents'),
    path('getimage/<int:id>', views.getimage, name='getimage'),
    path('editstudent/<int:id>', views.editstudent, name='editstudent'),
    path('searchbyclass/<int:id>', views.searchbyclass, name='searchbyclass'),

]