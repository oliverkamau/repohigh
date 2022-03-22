"""schoolsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from schoolsys import settings
from schoolsys.views import custom404
from . import views

handler404 = custom404

urlpatterns = [

                  path('', include('localities.urls')),
                  path('localities/', include('localities.urls')),
                  path('getrefreshtime/', views.getrefreshtime, name="getrefreshtime"),
                  path('setups/', include('setups.urls')),
                  path('login/', include('login.urls')),
                  path('studentmanager/', include('studentmanager.urls')),
                  path('useradmin/', include('useradmin.urls')),
                  path('staff/', include('staff.urls')),
                  path('exams/', include('exams.urls')),
                  path('fees/', include('feemanager.urls')),
                  path('finance/', include('financemanager.urls')),
                  path('timetabling/', include('timetabling.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
