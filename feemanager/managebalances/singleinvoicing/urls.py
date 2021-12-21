from django.urls import path
from . import views
urlpatterns = [

    path('singleinvoicepage', views.singleinvoicepage, name='singleinvoicepage'),
    path('searchstudents', views.searchstudents, name='searchstudents'),
    path('getfeestandardcharges/<int:id>', views.getfeestandardcharges, name='getfeestandardcharges'),
    path('updatebalancetracker', views.updatebalancetracker, name='updatebalancetracker'),

]