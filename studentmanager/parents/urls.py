from django.urls import path

from studentmanager.parents import views

urlpatterns = [
    path('getparent', views.getparent, name='getparent'),
    path('importexcel',views.importexcel,name='importexcel'),
    path('downloadexcel', views.generateExcel, name='downloadexcel'),
    path('searchproffession', views.searchproffession, name='searchproffession'),
    path('addparents', views.addparents, name='addparents'),
    path('getparents', views.getparents, name='getparents'),
    path('editparents/<int:id>', views.editparents, name='editparents'),
	path('updateparents/<int:id>', views.updateparents, name='updateparents'),
	path('deleteparents/<int:id>', views.deleteparents, name='deleteparents')

]