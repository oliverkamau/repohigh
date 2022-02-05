from django.urls import path

from . import views

urlpatterns = [
	path(r'getorgpage', views.getorgpage,name="getorgpage"),
    path(r'addorganization', views.createorganization, name="addorganization"),
    path(r'getorganizations', views.getorganizations, name="getorganizations"),
    path('editorganization/<int:id>', views.editorganization, name='editorganization'),
    path('updateorganization/<int:id>', views.updateorganization, name='updateorganization'),
    path('deleteorganization/<int:id>', views.deleteorganization, name='deleteorganization'),

]