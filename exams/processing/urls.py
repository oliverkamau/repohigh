from django.urls import path
from . import views
urlpatterns = [

    path('examprocess', views.examprocess, name='examprocess'),
    path('searchexamterm', views.searchexamterm, name='searchexamterm'),
    path('searchexamregister/<int:term>/<int:year>', views.searchexamregister, name='searchexamregister'),
    path('searchexamyear', views.searchexamyear, name='searchexamyear'),
    path('searchclasses', views.searchclasses, name='searchclasses'),
    path('searchteachers', views.searchteachers, name='searchteachers'),
    path('searchsubjects/<int:classcode>/<int:teacher>', views.searchsubjects, name='searchsubjects'),
    path('searchstudents/<int:classcode>/<int:subjects>', views.searchstudents, name='searchstudents'),
    path('getgradingscheme/<int:id>', views.getgradingscheme, name='getgradingscheme'),
    path('processgrade', views.processgrade, name='processgrade'),
    path('saveexammarks', views.saveexammarks, name='saveexammarks'),
    path('getrecordedmarks', views.getrecordedmarks, name='getrecordedmarks'),
    path('getexamrecordedmarks/<int:id>', views.getexamrecordedmarks, name='getexamrecordedmarks'),

    path('editmarks/<int:id>', views.editmarks, name='editmarks'),
    path('updateexammarks/<int:id>', views.updateexammarks, name='updateexammarks'),
    path('deleteexammarks/<int:id>', views.deleteexammarks, name='deleteexammarks'),
    path('importmarks', views.importmarks, name='importmarks'),
    path('dynamicaddress', views.dynamicaddress, name='dynamicaddress'),
    path('downloadmarksexcel', views.downloadmarksexcel, name='downloadmarksexcel'),

]