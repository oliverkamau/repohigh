from django.urls import path,include


urlpatterns = [

	path(r'days/', include('timetabling.daysetups.urls')),
	path(r'lessons/', include('timetabling.lessonsetups.urls')),
	path(r'allocation/', include('timetabling.lessonallocation.urls')),

]