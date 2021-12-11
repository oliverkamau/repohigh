from django.urls import path, include

urlpatterns = [
	path(r'registration/', include('exams.registration.urls')),
	path(r'processing/', include('exams.processing.urls'))

]