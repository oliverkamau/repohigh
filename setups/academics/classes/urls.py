from django.urls import path

from setups.academics.classes import views

urlpatterns = [
	path(r'getclass', views.classes,name="getclass"),
    path(r'createclass', views.createclass, name="createclass"),
    path(r'getclasses', views.getclasses, name="getclasses"),
    path('editclasses/<int:id>', views.editclasses, name='editclasses'),
    path('updateclasses/<int:id>', views.updateclasses, name='updateclasses'),
    path('deleteclasses/<int:id>', views.deleteclasses, name='deleteclasses'),
    path('searchteachers', views.searchteachers, name='searchteachers'),
    path('searchclasses', views.searchclasses, name='searchclasses')

]