from django.urls import path
from . import views
urlpatterns = [

    path('examreg', views.examreg, name='examreg'),
    path('searchexamtype', views.searchexamtype, name='searchexamtype'),
    path('searchexamterm', views.searchexamterm, name='searchexamterm'),
    path('searchexamgrading', views.searchexamgrading, name='searchexamgrading'),
    path('searchexamyear', views.searchexamyear, name='searchexamyear'),
    path(r'createregister', views.createexamreg, name="createregister"),
    path(r'getexamreg', views.getexamreg, name="getexamreg"),
    path(r'editexamreg/<int:id>', views.editexamreg, name='editexamreg'),
    path(r'updateregister/<int:id>', views.updateregister, name='updateregister'),
    path(r'deleteexam/<int:id>', views.deleteexam, name='deleteexam'),

]