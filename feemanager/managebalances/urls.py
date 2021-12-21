from django.urls import path, include
from . import views
urlpatterns = [

    path('balances', views.balances, name='balances'),
    path(r'setups/', include('feemanager.managebalances.singleinvoicing.urls')),

]