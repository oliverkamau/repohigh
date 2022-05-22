from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name= 'home'),
    path('genderdata', views.genderdata, name='genderdata'),
    path('classdata', views.classdata, name='classdata'),
    path('feebalances', views.feebalances, name='feebalances'),
    path('paymentmodes', views.paymentmodes, name='paymentmodes'),


    # path('country',views.country,name='country'),
    # path('county', views.county, name='county'),
    # path('add', views.add, name='add'),
    # path('getStudents', views.getStudents, name='getStudents'),
    # path('addCountry', views.addcountry, name='addcountry'),
    # # path('getCountries', views.getcountry, name='getcountry'),
    # path('addCounty', views.addcounty, name='addcounty'),
    # path('getCounties', views.getcounty, name='getcounty'),
    # path('searchStudents', views.searchStudents, name='searchStudents'),
    # path('searchCounties/<int:id>', views.searchcounties, name='searchcounties'),
    # path('searchCountries', views.searchcountries, name='searchcountries'),
    # path('editStudent/<int:id>', views.editStudent, name='editStudent'),
    # path('update/<int:id>', views.updateStudent, name='updateStudent'),
    # path('deleteStudent/<int:id>', views.deleteStudent, name='deleteStudent')

]