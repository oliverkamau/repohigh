from django.urls import path

from . import views

urlpatterns = [
    path('studentpage', views.studentpage, name='studentpage'),
    path('addstudent', views.addstudent, name='addstudent'),
    path('getstatistics', views.getstatistics, name='getstatistics'),
    path('getstudents', views.getstudents, name='getstudents'),
    path('editstudent/<int:id>', views.editstudent, name='editstudent'),
    path('updatestudent/<int:id>', views.updatestudent, name='updatestudent'),
    path('deletestudent/<int:id>', views.deletestudent, name='deletestudent'),
    path('uploadstudentdocs', views.uploadstudentdocs, name='uploadstudentdocs'),
    path('viewstudentdocs', views.viewdocs, name='viewstudentdocs'),
    path('deletestudentdocs', views.deletestudentdocs, name='deletestudentdocs'),
    path('searchclasses', views.searchclasses, name='searchclasses'),
    path('searchparent', views.searchparent, name='searchparent'),
    path('searchfeecategory', views.searchfeecategory, name='searchfeecategory'),
    path('searchdorms', views.searchdorms, name='searchdorms'),
    path('searchcampus', views.searchcampus, name='searchcampus'),
    path('searchyears', views.searchyears, name='searchyears'),
    path('searchstudentstatus', views.searchstudentstatus, name='searchstudentstatus'),
    path('searchhealthstatus', views.searchhealthstatus, name='searchhealthstatus'),
    path('searchdocs', views.searchdocs, name='searchdocs'),
    path('searchcountry', views.searchcountry, name='searchcountry'),
    path('searchdenominations', views.searchdenominations, name='searchdenominations'),
    path('searchcounties/<int:id>', views.searchcounties, name='searchcounties'),
    path('searchsubcounty/<int:id>', views.searchsubcounty, name='searchsubcounty'),
    path('searchlocation/<int:id>', views.searchlocation, name='searchlocation'),
    path('searchsublocation/<int:id>', views.searchsublocation, name='searchsublocation'),
    path('searchvillage/<int:id>', views.searchvillage, name='searchvillage'),
    path('searchstudentsources', views.searchstudentsources, name='searchstudentsources'),
    path('getleaveoutsurl/<int:id>', views.getleaveoutsurl, name='getleaveoutsurl'),



]