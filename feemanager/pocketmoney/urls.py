from django.urls import path
from . import views
urlpatterns = [

    path('pocketmoneypage', views.pocketmoneypage, name='pocketmoneypage'),
    path('searchclass', views.searchclass, name='searchclass'),
    path('searchstudents', views.searchstudents, name='searchstudents'),
    path('savepocketmoney', views.savepocketmoney, name='savepocketmoney'),
    path('getbalance/<int:id>', views.getbalance, name='getbalance'),



]