from django.urls import path
from . import views
urlpatterns = [

    path('groupingpage', views.groupingpage, name='groupingpage'),
    path('searchfeecategory', views.searchfeecategory, name='searchfeecategory'),
    path('searchnewfeecategory', views.searchnewfeecategory, name='searchnewfeecategory'),
    path('searchclass', views.searchclass, name='searchclass'),
    path('getclassstudents/<int:id>', views.getclassstudents, name='getclassstudents'),
    path('getfeestudents/<int:id>/<int:classcode>', views.getfeestudents, name='getfeestudents'),
    path('getfeestudent/<int:id>', views.getfeestudent, name='getfeestudent'),
    path('getnewfeestudents/<int:id>/<int:classcode>', views.getnewfeestudents, name='getnewfeestudents'),
    path('getnewfeestudent/<int:id>', views.getnewfeestudent, name='getnewfeestudent'),
    path('dynamicaddress', views.dynamicaddress, name='dynamicaddress'),
    path('assigncategory', views.assignstudentcategory, name='assigncategory'),
    path('unassigncategory', views.unassignstudentcategory, name='unassigncategory'),
    path('unassignallcategories', views.unassignallcategories, name='unassignallcategories'),
    path('assignallcategories', views.assignallcategories, name='assignallcategories'),


]