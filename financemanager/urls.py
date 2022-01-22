from django.urls import path, re_path, include

urlpatterns = [
    path(r'pettysetups/', include('financemanager.pettycashsetups.urls')),

]