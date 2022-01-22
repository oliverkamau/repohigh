from django.urls import path
from . import views
urlpatterns = [

    path('replenishpage', views.replenishpage, name='replenishpage'),
    path('searchaccount', views.searchaccount, name='searchaccount'),
    path('searchusers', views.searchusers, name='searchusers'),
    path('balance/<int:id>', views.balance, name='balance'),
    path('geteditfloat/<int:id>', views.geteditfloat, name='geteditfloat'),
    path('float/<int:id>', views.float, name='float'),
    path('savefloatcash', views.savefloatcash, name='savefloatcash'),
    path('getfloatgrid', views.getfloatgrid, name='getfloatgrid'),

]