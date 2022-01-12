from django.urls import path, include
from . import views
urlpatterns = [

    path('feesetupspage', views.feesetupspage, name='feesetupspage'),
    path(r'feestructure/', include('feemanager.feesetup.feestructure.urls')),
    path(r'feesgroup/', include('feemanager.feesetup.feegroups.urls')),

]