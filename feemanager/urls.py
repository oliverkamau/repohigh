from django.urls import path, include

urlpatterns = [
	path(r'setups/', include('feemanager.feesetup.urls')),
	path(r'manage/', include('feemanager.managebalances.urls')),
	path(r'recieve/', include('feemanager.recievefees.urls')),
	path(r'pocket/', include('feemanager.pocketmoney.urls')),

]