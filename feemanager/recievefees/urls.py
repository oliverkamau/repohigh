from django.urls import path
from . import views
urlpatterns = [

    path('feepage', views.feepage, name='feepage'),
    path('getfeestandardcharges', views.getfeestandardcharges, name='getfeestandardcharges'),
    path('searchclass', views.searchclass, name='searchclass'),
    path('searchstudents', views.searchstudents, name='searchstudents'),
    path('searchstudents/<int:id>', views.searchstudents, name='searchstudents'),
    path('searchmodes', views.searchmodes, name='searchmodes'),
    path('searchbanks', views.searchbanks, name='searchbanks'),
    path('searchterm', views.searchterm, name='searchterm'),
    path('getrackerbalances/<int:id>', views.getfeestudentcharges, name='getfeestudentcharges'),
    path('recievefees', views.recievefees, name='recievefees'),
    path('currentterm', views.currentterm, name='currentterm'),
    path('feedistribution', views.feedistribution, name='feedistribution'),
]