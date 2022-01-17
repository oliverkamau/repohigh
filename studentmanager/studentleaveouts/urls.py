from django.urls import path

from . import views

urlpatterns = [
    path('leaveoutspage', views.leaveoutspage, name='leaveoutspage'),
    path('searchclasses', views.searchclasses, name='searchclasses'),
    path('getunassignedstudents/<int:id>', views.getunassignedstudents,
         name='getunassignedstudents'),
    path('getassignedstudents/<int:id>', views.getassignedleavestudents,
         name='getassignedstudents'),
    path('getindividualstudent/<int:id>', views.getindividualstudent,
         name='getindividualstudent'),
    path('getindividualleavestudent/<int:id>', views.getindividualleavestudent,
         name='getindividualleavestudent'),
    path('dynamicaddress', views.dynamicaddress, name='dynamicaddress'),
    path('assignleaveouts', views.assignleaveouts, name='assignleaveouts'),
    path('unassignleaveouts', views.unassignleaveouts, name='unassignleaveouts'),
    path('unassignbulkleaves', views.unassignbulkleaves, name='unassignbulkleaves'),
    path('assignbulkleaves', views.assignbulkleaves, name='assignbulkleaves'),
    path('unassignallleaveouts', views.unassignallleaveouts, name='unassignallleaveouts'),
    path('assignallleaveouts', views.assignallleaveouts, name='assignallleaveouts'),
    path('assignallleaveouts', views.assignallleaveouts, name='assignallleaveouts'),
    path('getstudentsleaves', views.getstudentsleaves, name='getstudentsleaves'),
    path('editstudent/<int:id>', views.editstudent, name='editstudent'),


]