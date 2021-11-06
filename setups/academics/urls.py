from django.urls import path, include

urlpatterns = [
	path(r'classes/', include('setups.academics.classes.urls')),
	path(r'termdates/', include('setups.academics.termdates.urls'))
]