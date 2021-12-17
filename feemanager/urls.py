from django.urls import path, include

urlpatterns = [
	path(r'setups/', include('feemanager.feesetup.urls')),

]