from django.urls import path, include

urlpatterns = [
	path(r'registration/', include('exams.registration.urls'))

]