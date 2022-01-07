from django.urls import path
from . import views
urlpatterns = [

    path('structurepage', views.structurepage, name='structurepage'),
    path('searchexamterm', views.searchexamterm, name='searchexamterm'),
    path('searchfeecategory', views.searchfeecategory, name='searchfeecategory'),
    path('getfeestandardcharges', views.getfeestandardcharges, name='getfeestandardcharges'),
    path('addfeestructure', views.addfeestructure, name='addfeestructure'),
    path('getfeestructures', views.getfeestructures, name='getfeestructures'),
    path('editfeestructure/<int:id>', views.editfeestructure, name='editfeestructure'),
    path('updatefeestructure/<int:id>', views.updatefeestructure, name='updatefeestructure'),
    path('deletefeestructure/<int:id>', views.deletefeestructure, name='deletefeestructure'),


]