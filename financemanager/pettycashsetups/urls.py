from django.urls import path, include
from . import views
urlpatterns = [

    path('pettypage', views.pettypage, name='pettypage'),
    path(r'pettycash/', include('financemanager.pettycashsetups.pettycashpayments.urls')),
    path(r'float/', include('financemanager.pettycashsetups.floatreplenishment.urls')),

    # path(r'feesgroup/', include('feemanager.feesetup.feegroups.urls')),

]