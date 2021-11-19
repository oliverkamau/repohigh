from django.urls import path, include

from studentmanager.parents import views

urlpatterns = [
	path(r'parents/', include('studentmanager.parents.urls')),
	path(r'students/', include('studentmanager.student.urls')),
	path(r'subjects/', include('studentmanager.studentsubjects.urls'))

]