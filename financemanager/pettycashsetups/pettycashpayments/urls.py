from django.urls import path
from . import views
urlpatterns = [

    path('paymentpage', views.paymentpage, name='paymentpage'),
    path('searchaccount', views.searchaccount, name='searchaccount'),
    path('searchusers', views.searchusers, name='searchusers'),
    path('savepettycash', views.savepettycash, name='savepettycash'),
    path('getpettycashgrid', views.getpettycashgrid, name='getpettycashgrid'),
    path('geteditpetty/<int:id>', views.geteditpetty, name='geteditpetty'),



]