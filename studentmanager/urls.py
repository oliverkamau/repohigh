from django.urls import path, include

from studentmanager.parents import views

urlpatterns = [
	path(r'parents/', include('studentmanager.parents.urls'))

	]